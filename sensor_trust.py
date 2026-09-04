from typing import Dict, Any, List
import time

class SensorTrustEngine:
    def __init__(self):
        # Initial simulated sensor network (48 sensors across pilot district)
        self.sensors = self._init_sensors()

    def _init_sensors(self) -> Dict[str, Dict[str, Any]]:
        sensors = {}
        # 16 River Gauges
        for i in range(1, 17):
            sensors[f"R-{i:02d}"] = {
                "id": f"R-{i:02d}",
                "name": f"River Ultrasound Node #{i}",
                "type": "river_gauge",
                "location": f"Sector {chr(65 + (i % 4))}-Riverbank",
                "value": round(2.1 + (i % 3) * 0.4, 2),
                "unit": "m",
                "last_values": [2.0, 2.05, 2.1],
                "trust_score": 98,
                "status": "ONLINE",
                "battery": 94 - (i % 8),
                "last_seen_sec_ago": 4,
                "anomaly": None
            }
        # 16 Rain Gauges (NASA IMERG / Tipping Bucket)
        for i in range(1, 17):
            sensors[f"RG-{i:02d}"] = {
                "id": f"RG-{i:02d}",
                "name": f"Optical Rain Gauge #{i}",
                "type": "rain_gauge",
                "location": f"High Ridge Sector {chr(65 + (i % 4))}",
                "value": round(15.0 + (i % 4) * 6.0, 1),
                "unit": "mm/h",
                "last_values": [12.0, 14.0, 15.0],
                "trust_score": 99,
                "status": "ONLINE",
                "battery": 97 - (i % 6),
                "last_seen_sec_ago": 2,
                "anomaly": None
            }
        # 12 Soil Moisture Probes
        for i in range(1, 13):
            sensors[f"SM-{i:02d}"] = {
                "id": f"SM-{i:02d}",
                "name": f"FDR Soil Moisture Probe #{i}",
                "type": "soil_probe",
                "location": f"Catchment Slope {chr(65 + (i % 4))}",
                "value": round(45.0 + (i % 5) * 8.0, 1),
                "unit": "%",
                "last_values": [40.0, 43.0, 45.0],
                "trust_score": 96,
                "status": "ONLINE",
                "battery": 89 - (i % 7),
                "last_seen_sec_ago": 6,
                "anomaly": None
            }
        # 4 LoRa Mesh Gateways
        for i in range(1, 5):
            sensors[f"GW-{i:02d}"] = {
                "id": f"GW-{i:02d}",
                "name": f"LoRaWAN Mountain Gateway #{i}",
                "type": "gateway",
                "location": f"Peak Tower {chr(65 + i)}",
                "value": 100.0,
                "unit": "% uptime",
                "last_values": [100.0, 100.0, 100.0],
                "trust_score": 100,
                "status": "ONLINE",
                "battery": 100,
                "last_seen_sec_ago": 1,
                "anomaly": None
            }
        return sensors

    def evaluate_sensor_reading(self, sensor_id: str, new_value: float) -> Dict[str, Any]:
        if sensor_id not in self.sensors:
            return {"error": "Sensor not found"}

        sensor = self.sensors[sensor_id]
        history = sensor["last_values"]
        history.append(new_value)
        if len(history) > 10:
            history.pop(0)

        # Anomaly detection checks:
        anomaly = None
        trust_score = 100
        status = "ONLINE"

        # 1. Extreme Spike / Out of physics bounds
        if sensor["type"] == "river_gauge":
            if new_value > 15.0 or (len(history) >= 2 and abs(new_value - history[-2]) > 5.0):
                anomaly = f"Sudden impossible spike from {history[-2]}m to {new_value}m in 10s"
                trust_score = 24
                status = "POSSIBLE_FAILURE"
        elif sensor["type"] == "rain_gauge":
            if new_value > 300.0 or new_value < 0:
                anomaly = f"Out-of-range rain reading {new_value} mm/h"
                trust_score = 30
                status = "DEGRADED"
        elif sensor["type"] == "soil_probe":
            if new_value > 100.0 or new_value < 0:
                anomaly = f"Impossible soil saturation {new_value}%"
                trust_score = 15
                status = "FAULT"

        # Update sensor record
        sensor["value"] = new_value
        sensor["trust_score"] = trust_score
        sensor["status"] = status
        sensor["anomaly"] = anomaly

        return sensor

    def get_network_health(self) -> Dict[str, Any]:
        total = len(self.sensors)
        online = sum(1 for s in self.sensors.values() if s["status"] in ["ONLINE", "DEGRADED"])
        anomalies = [s for s in self.sensors.values() if s["anomaly"] is not None]
        avg_trust = round(sum(s["trust_score"] for s in self.sensors.values()) / total, 1)

        return {
            "total_sensors": total,
            "online_sensors": online,
            "offline_sensors": total - online,
            "average_trust_score": avg_trust,
            "anomalies_detected": len(anomalies),
            "anomaly_list": anomalies,
            "gateway_mesh_status": "LORA_MESH_ACTIVE",
            "cloud_sync": "SYNCED_REALTIME",
            "sensors": list(self.sensors.values())
        }
