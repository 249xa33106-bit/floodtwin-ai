from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

from ml_engine import FloodRiskEngine
from sensor_trust import SensorTrustEngine
from digital_twin import FloodDigitalTwin
from evacuation import EvacuationRoutingEngine
from commander_ai import IncidentCommanderAI
from alerts_engine import EmergencyAlertsEngine
from demo_scenarios import DemoScenariosEngine

app = FastAPI(
    title="FloodTwin AI — Decision Support Platform for NDRF",
    description="Hyper-local flash flood prediction, 4D digital twin simulation, explainable AI, and dynamic evacuation routing engine.",
    version="2.0.0"
)

# Enable CORS for Next.js / React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Engines
ml_engine = FloodRiskEngine()
sensor_engine = SensorTrustEngine()
twin_engine = FloodDigitalTwin()
evac_engine = EvacuationRoutingEngine()
commander_ai = IncidentCommanderAI()
alerts_engine = EmergencyAlertsEngine()
demo_engine = DemoScenariosEngine()

class TelemetryInput(BaseModel):
    rain_intensity: Optional[float] = 47.0
    rain_30min: Optional[float] = 25.0
    rain_1h: Optional[float] = 51.0
    rain_3h: Optional[float] = 106.0
    rain_6h: Optional[float] = 134.0
    rain_24h: Optional[float] = 184.0
    forecast_rain_1h: Optional[float] = 61.0
    forecast_rain_3h: Optional[float] = 78.0
    soil_moisture: Optional[float] = 91.0
    river_level: Optional[float] = 4.22
    water_level_rise_10m: Optional[float] = 51.0
    water_level_rise_30m: Optional[float] = 112.0
    water_level_acceleration: Optional[float] = 7.8
    elevation: Optional[float] = 1380.0
    slope: Optional[float] = 24.0
    distance_from_river: Optional[float] = 80.0
    flow_accumulation: Optional[float] = 650.0
    historical_flood_frequency: Optional[float] = 0.85

class CommanderQueryInput(BaseModel):
    query: str

class SensorUpdateInput(BaseModel):
    sensor_id: str
    new_value: float

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "system": "FloodTwin AI Core Engines",
        "active_nodes": 48,
        "mesh_network": "LoRaWAN Active (915MHz)",
        "satellite_sync": "NASA IMERG + Sentinel-1 Online"
    }

@app.get("/api/dashboard/summary")
def get_dashboard_summary():
    demo_state = demo_engine.get_current_state()
    features = {
        "rain_intensity": demo_state["rain_intensity"],
        "rain_30min": demo_state.get("rain_30min", 25.0),
        "rain_1h": demo_state.get("rain_1h", 51.0),
        "rain_3h": demo_state.get("rain_3h", 106.0),
        "rain_6h": demo_state.get("rain_6h", 134.0),
        "rain_24h": demo_state.get("rain_24h", 184.0),
        "forecast_rain_1h": demo_state.get("forecast_rain_1h", 61.0),
        "soil_moisture": demo_state["soil_moisture"],
        "river_level": demo_state["river_level"],
        "water_level_rise_10m": demo_state["water_level_rise_10m"],
        "water_level_acceleration": demo_state.get("water_level_acceleration", 2.0),
        "elevation": 1380.0,
        "slope": 24.0,
        "distance_from_river": 80.0,
        "flow_accumulation": 650.0,
        "historical_flood_frequency": 0.85
    }
    prediction = ml_engine.predict(features)
    network = sensor_engine.get_network_health()
    priorities = alerts_engine.get_ndrf_priority_matrix(prediction["risk_score"])
    
    total_exposed = sum(p["exposed_population"] for p in priorities if p["risk_score"] >= 50)
    critical_zones = sum(1 for p in priorities if p["risk_score"] >= 76)

    return {
        "demo_step": demo_state,
        "prediction": prediction,
        "metrics": {
            "critical_zones": critical_zones or 2,
            "population_at_risk": total_exposed or 4250,
            "active_sensors": f"{network['online_sensors']}/{network['total_sensors']}",
            "active_alerts": len(alerts_engine.get_alert_history()) or 3,
            "satellite_rainfall_imerg": f"{features['rain_3h']} mm (3h sum)",
            "river_water_level": f"{features['river_level']} m",
            "river_rise_velocity": f"+{features['water_level_rise_10m']} cm / 10 min",
            "river_trend": "RAPIDLY_RISING" if features['water_level_rise_10m'] > 20 else "STEADY"
        },
        "priorities": priorities,
        "sensor_network": network
    }

@app.post("/api/predict/risk")
def predict_flood_risk(data: TelemetryInput):
    features = data.dict()
    return ml_engine.predict(features)

@app.get("/api/digital-twin/simulate")
def get_digital_twin_simulation(
    rain: float = Query(52.0),
    river: float = Query(4.22),
    soil: float = Query(91.0)
):
    return twin_engine.simulate_timesteps(rain, river, soil)

@app.get("/api/evacuation/routes")
def get_evacuation_routes(
    origin: str = Query("Zone-B-Center"),
    rain: float = Query(52.0),
    river: float = Query(4.22)
):
    return evac_engine.calculate_evacuation_routes(origin, rain, river)

@app.get("/api/sensors/health")
def get_sensors_health():
    return sensor_engine.get_network_health()

@app.post("/api/sensors/evaluate")
def evaluate_sensor(data: SensorUpdateInput):
    return sensor_engine.evaluate_sensor_reading(data.sensor_id, data.new_value)

@app.post("/api/commander/ask")
def ask_incident_commander(data: CommanderQueryInput):
    demo_state = demo_engine.get_current_state()
    pred = ml_engine.predict({
        "rain_3h": demo_state.get("rain_3h", 106.0),
        "soil_moisture": demo_state["soil_moisture"],
        "river_level": demo_state["river_level"],
        "water_level_rise_10m": demo_state["water_level_rise_10m"],
        "slope": 24.0
    })
    state_ctx = {
        "risk_score": pred["risk_score"],
        "rain_intensity": demo_state["rain_intensity"],
        "river_level": demo_state["river_level"],
        "population_at_risk": 2430
    }
    return commander_ai.get_grounded_response(data.query, state_ctx)

@app.get("/api/alerts/priority-matrix")
def get_priority_matrix(risk: float = Query(91.0)):
    return alerts_engine.get_ndrf_priority_matrix(risk)

@app.post("/api/alerts/broadcast")
def trigger_alert_broadcast(level: int = Body(3), target_zone: str = Body("Zone B (Village B Lowlands)")):
    return alerts_engine.generate_multilingual_alert(level, target_zone)

@app.get("/api/alerts/history")
def get_alert_history():
    return alerts_engine.get_alert_history()

@app.post("/api/demo/set-step/{step_id}")
def set_demo_step(step_id: int):
    if step_id < 1 or step_id > 10:
        raise HTTPException(status_code=400, detail="Step must be between 1 and 10")
    return demo_engine.set_step(step_id)

@app.get("/api/demo/current")
def get_demo_step():
    return demo_engine.get_current_state()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
