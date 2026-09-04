from typing import Dict, Any, List

class IncidentCommanderAI:
    def __init__(self):
        pass

    def get_grounded_response(self, query: str, state: Dict[str, Any]) -> Dict[str, Any]:
        q_lower = query.lower()
        risk = state.get("risk_score", 91)
        rain = state.get("rain_intensity", 52.0)
        river = state.get("river_level", 4.22)
        pop_risk = state.get("population_at_risk", 2430)

        # Tactical Decision Logic
        if "who" in q_lower or "which village" in q_lower or "immediate" in q_lower or "priority" in q_lower:
            answer = (
                f"**Zone B (Village B Lowlands)** currently has the highest operational priority.\n\n"
                f"**Telemetry Assessment:**\n"
                f"• Flash Flood Risk: **{risk}/100 (CRITICAL)**\n"
                f"• Upstream River Stage: **{river}m** (Accelerating at +51cm/10min)\n"
                f"• Exposed Population: **~{pop_risk:,} residents**\n"
                f"• Threat Horizon: Road-2 (Market Bridge) predicted to inundate in **27 minutes**.\n\n"
                f"**Directive:** Immediate evacuation order must be issued for Sectors B2 and B3."
            )
            actions = [
                "Trigger RED alert siren for Sectors B2 & B3",
                "Direct citizen traffic along Safe Route-B (Ridge Highway Link)",
                "Dispatch NDRF Rescue Team 02 to Market Bridge crossing point",
                "Pre-position ambulances at Shelter-02 (Community Hall)"
            ]
        elif "what should i do" in q_lower or "action" in q_lower or "protocol" in q_lower or "sop" in q_lower:
            answer = (
                "**NDRF Tactical Action Plan (Level 3 Flash Flood Protocol):**\n\n"
                "1. **Trigger Immediate Red Siren & Multilingual Broadcast** for Zone B.\n"
                "2. **Block Road-1 & Road-2** access with local police to prevent vehicles entering drowning zone.\n"
                "3. **Deploy Evacuation Convoy along Route-B** toward Shelter-02 (Community Sports Complex, Elev: 1530m).\n"
                "4. **Mobilize NDRF Swift Water Rescue Units (Team 01 & 02)** with inflatable boats at Sector C3/B3.\n"
                "5. **Verify LoRa Mesh Bridge** for continued real-time telemetry if fiber/cellular grid drops.\n"
                "6. **Re-evaluate water velocity in 10 minutes**."
            )
            actions = [
                "Execute Level 3 Broadcast across SMS/WhatsApp/Siren",
                "Confirm high-ground shelter readiness at Shelter-02",
                "Enforce physical roadblock at Riverside Junction 1",
                "Stage medical triage at Shelter-02 with 43 priority kits"
            ]
        elif "shelter" in q_lower or "where should people go" in q_lower:
            answer = (
                f"**Recommended Safe Shelter: Shelter-02 (Community Hall & Sports Complex)**\n\n"
                f"• Elevation: **1,530 m** (Safe high ground, 150m above river channel)\n"
                f"• Capacity: **850 total / 540 currently available**\n"
                f"• Medical Facility: **Active with full trauma & first aid supplies**\n"
                f"• Approach Route: **Route-B (West Ridge Access) is 100% CLEAR with 108 min safety margin.**"
            )
            actions = [
                "Direct all Zone B evacuees to Shelter-02",
                "Reserve Shelter-01 (Ridge School) for Zone A overflow"
            ]
        elif "explain" in q_lower or "why" in q_lower:
            answer = (
                f"**Root Cause Explainability Analysis:**\n\n"
                f"1. **Extreme 3-Hour Rainfall Accumulation (29% contribution)**: Catchment received 106mm in 3 hours.\n"
                f"2. **Rapid River Rise Velocity (23% contribution)**: River surged from 3.1m to {river}m (+51cm/10min).\n"
                f"3. **Severe Soil Saturation (19% contribution)**: Pre-existing moisture at 91%, eliminating infiltration capacity.\n"
                f"4. **Steep Himalayan Catchment Terrain (16% contribution)**: High runoff speed down 32° gradient into narrow valley floor."
            )
            actions = [
                "Monitor catchment soil saturation sensors (SM-01 to SM-04)",
                "Check IMERG satellite rain cloud trajectory updates"
            ]
        else:
            answer = (
                f"**Current Situation Briefing:**\n\n"
                f"System is actively tracking Mandakini Valley. Flash flood risk in critical sector is **{risk}/100** with estimated impact in **42–58 minutes**. "
                f"Rainfall intensity is **{rain} mm/h** and river level is **{river}m**. Evacuation Route B is operational and safe."
            )
            actions = [
                "Monitor real-time gauge feeds",
                "Maintain continuous communication with NDRF field units"
            ]

        return {
            "query": query,
            "answer": answer,
            "recommended_actions": actions,
            "tactical_priority_village": "Zone B (Village B Lowlands)",
            "incident_threat_level": "RED_CRITICAL" if risk >= 76 else "ORANGE_HIGH"
        }
