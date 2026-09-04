from typing import Dict, Any

class DemoScenariosEngine:
    def __init__(self):
        self.current_step = 1
        # Default telemetry baseline
        self.state = {
            "step": 1,
            "title": "STEP 1: Baseline Normal / Moderate Monitoring",
            "story_narration": "Village A is in Moderate status. System continuously fuses NASA IMERG rainfall, river gauges, soil moisture, and DEM topography.",
            "rain_intensity": 21.0,
            "rain_30min": 10.5,
            "rain_1h": 21.0,
            "rain_3h": 35.0,
            "rain_6h": 48.0,
            "rain_24h": 62.0,
            "forecast_rain_1h": 25.0,
            "forecast_rain_3h": 35.0,
            "soil_moisture": 42.0,
            "river_level": 2.70,
            "water_level_rise_10m": 4.0, # cm
            "water_level_rise_30m": 12.0, # cm
            "water_level_acceleration": 0.5,
            "selected_village": "Village A (Zone A)",
            "selected_grid": "A2",
            "active_timestep": "NOW"
        }

    def set_step(self, step: int) -> Dict[str, Any]:
        self.current_step = step
        
        if step == 1:
            self.state.update({
                "step": 1,
                "title": "STEP 1: Baseline Normal Situational Awareness",
                "story_narration": "The system continuously monitors multi-source rainfall, river stages, soil moisture, and terrain vulnerability. Village A is in Moderate status (Risk 43/100).",
                "rain_intensity": 21.0,
                "rain_3h": 35.0,
                "soil_moisture": 42.0,
                "river_level": 2.70,
                "water_level_rise_10m": 4.0,
                "water_level_acceleration": 0.5,
                "selected_village": "Village A (Zone A)",
                "selected_grid": "A2",
                "active_timestep": "NOW"
            })
        elif step == 2:
            self.state.update({
                "step": 2,
                "title": "STEP 2: Upstream Cloudburst Rainfall Surge (21 → 52 mm/hr)",
                "story_narration": "Intense convective storm detected by NASA IMERG & optical rain gauges. Rain surges rapidly from 21 mm/hr to 52 mm/hr. 3-hour accumulation hits 106mm.",
                "rain_intensity": 52.0,
                "rain_30min": 26.0,
                "rain_1h": 51.0,
                "rain_3h": 106.0,
                "rain_6h": 134.0,
                "rain_24h": 184.0,
                "forecast_rain_1h": 61.0,
                "soil_moisture": 78.0,
                "river_level": 3.10,
                "water_level_rise_10m": 18.0,
                "water_level_acceleration": 2.4,
                "selected_village": "Village B (Zone B)",
                "selected_grid": "B3",
                "active_timestep": "NOW"
            })
        elif step == 3:
            self.state.update({
                "step": 3,
                "title": "STEP 3: River Rapid Rise & Acceleration (+51 cm / 10 min)",
                "story_narration": "Mountain river level shoots from 3.10m to 4.22m with extreme acceleration (+51cm in 10 minutes). Soil moisture hits 91% saturation.",
                "rain_intensity": 52.0,
                "rain_3h": 106.0,
                "soil_moisture": 91.0,
                "river_level": 4.22,
                "water_level_rise_10m": 51.0, # +51 cm / 10 min
                "water_level_rise_30m": 112.0,
                "water_level_acceleration": 7.8, # Accelerating rise velocity
                "selected_village": "Village B (Zone B)",
                "selected_grid": "B3",
                "active_timestep": "NOW"
            })
        elif step == 4:
            self.state.update({
                "step": 4,
                "title": "STEP 4: AI Triggers CRITICAL Alert (Risk 91/100, Impact in 42–58 min)",
                "story_narration": "The hybrid XGBoost & deterministic safety model triggers RED CRITICAL warning (91/100) with estimated critical condition impact window in 42–58 minutes for 2,430 residents.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "soil_moisture": 91.0,
                "water_level_rise_10m": 51.0,
                "selected_village": "Village B (Zone B)",
                "selected_grid": "B3",
                "active_timestep": "NOW"
            })
        elif step == 5:
            self.state.update({
                "step": 5,
                "title": "STEP 5: Explainable AI — Why is the Risk Critical?",
                "story_narration": "Explainability Engine decomposes risk factors: Extreme 3h Rain (+29%), Rapid River Rise (+23%), Soil Saturation (+19%), Steep Upstream Terrain (+16%). Eliminates black-box distrust.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "soil_moisture": 91.0,
                "selected_village": "Village B (Zone B)",
                "selected_grid": "B3",
                "active_timestep": "NOW"
            })
        elif step == 6:
            self.state.update({
                "step": 6,
                "title": "STEP 6: 4D Future Flood Twin (NOW → +30m → +60m → +120m)",
                "story_narration": "Physics-based 250m grid simulation models dynamic water propagation. Authorities watch inundation expand across low-lying sectors over the next 120 minutes.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "soil_moisture": 91.0,
                "active_timestep": "+60m"
            })
        elif step == 7:
            self.state.update({
                "step": 7,
                "title": "STEP 7: Predictive Road Submersion Check — Road-2 Fails in 27 min!",
                "story_narration": "Traditional route (Road-1 → Road-2) is predicted to submerge in 27 minutes. Safety buffer is only 5 minutes. System flags Road-2 as CRITICALLY UNSAFE.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "active_timestep": "+30m"
            })
        elif step == 8:
            self.state.update({
                "step": 8,
                "title": "STEP 8: Flood-Aware Evacuation Optimizer Selects Safe Route B",
                "story_narration": "A* Evacuation Router rejects flooded Road-2 and computes Safe Route B along the western ridge to Shelter-02 (Community Sports Complex) with a 108 min safety margin!",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "active_timestep": "NOW"
            })
        elif step == 9:
            self.state.update({
                "step": 9,
                "title": "STEP 9: Multilingual Emergency Broadcast & Siren Dispatch",
                "story_narration": "Automated Level 3 alerts broadcast simultaneously in Hindi, English, and regional languages to 1,843 resident endpoints and NDRF battalions.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "active_timestep": "NOW"
            })
        elif step == 10:
            self.state.update({
                "step": 10,
                "title": "STEP 10: NDRF AI Incident Commander Grounded Operational Briefing",
                "story_narration": "'FloodTwin AI doesn't stop at predicting a disaster. It converts prediction into an actionable evacuation decision.' Complete grounded situation report ready for command action.",
                "rain_intensity": 52.0,
                "river_level": 4.22,
                "active_timestep": "NOW"
            })
        
        return self.state

    def get_current_state(self) -> Dict[str, Any]:
        return self.state
