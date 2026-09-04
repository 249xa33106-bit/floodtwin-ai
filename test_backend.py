import pytest
from fastapi.testclient import TestClient
from main import app
from ml_engine import FloodRiskEngine
from sensor_trust import SensorTrustEngine
from digital_twin import FloodDigitalTwin
from evacuation import EvacuationRoutingEngine

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

def test_ml_risk_engine():
    engine = FloodRiskEngine()
    features = {
        "rain_3h": 106.0,
        "soil_moisture": 91.0,
        "river_level": 4.22,
        "water_level_rise_10m": 51.0,
        "slope": 24.0,
        "forecast_rain_1h": 61.0,
        "distance_from_river": 80.0
    }
    pred = engine.predict(features)
    assert "risk_score" in pred
    assert pred["risk_score"] >= 76.0 # Critical
    assert pred["risk_level"] == "CRITICAL"
    assert len(pred["explanations"]) > 0
    assert "lead_time_range" in pred

def test_sensor_trust_anomaly_detection():
    engine = SensorTrustEngine()
    # Test impossible sudden spike
    anomaly_res = engine.evaluate_sensor_reading("R-01", 18.5)
    assert anomaly_res["trust_score"] < 50
    assert anomaly_res["status"] == "POSSIBLE_FAILURE"
    assert "spike" in anomaly_res["anomaly"].lower()

def test_digital_twin_timesteps():
    twin = FloodDigitalTwin()
    res = twin.simulate_timesteps(rain_intensity=52.0, river_level=4.22, soil_saturation=91.0)
    sim = res["simulation"]
    assert "NOW" in sim
    assert "+30m" in sim
    assert "+60m" in sim
    assert "+120m" in sim
    assert sim["+120m"]["flooded_cells_count"] >= sim["NOW"]["flooded_cells_count"]

def test_evacuation_routing():
    evac = EvacuationRoutingEngine()
    routes_res = evac.calculate_evacuation_routes(origin="Zone-B-Center", rain_intensity=52.0, river_level=4.22)
    assert "routes" in routes_res
    routes = routes_res["routes"]
    route_a = next(r for r in routes if r["id"] == "ROUTE-A")
    route_b = next(r for r in routes if r["id"] == "ROUTE-B")
    assert route_a["verdict"] == "UNSAFE" # Road-2 will submerge
    assert route_b["verdict"] == "SAFEST_RECOMMENDED"
    assert route_b["safety_margin_min"] > 30

def test_incident_commander():
    res = client.post("/api/commander/ask", json={"query": "Which village needs immediate evacuation?"})
    assert res.status_code == 200
    data = res.json()
    assert "Village B" in data["answer"] or "Zone B" in data["answer"]
    assert len(data["recommended_actions"]) > 0

def test_demo_step_progression():
    res = client.post("/api/demo/set-step/4")
    assert res.status_code == 200
    assert res.json()["step"] == 4
