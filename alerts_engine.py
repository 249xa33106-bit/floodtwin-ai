from typing import Dict, Any, List
import datetime

class EmergencyAlertsEngine:
    def __init__(self):
        self.alert_history = []

    def get_ndrf_priority_matrix(self, current_risk: float = 91.0) -> List[Dict[str, Any]]:
        # Calculate response priority score: (Risk * Population / ETA_factor)
        villages = [
            {
                "rank": 1,
                "village": "Village B (Sectors B2/B3 Lowlands)",
                "risk_score": int(current_risk),
                "risk_badge": "🔴 CRITICAL",
                "exposed_population": 2430,
                "vulnerable_groups": {"children": 410, "elderly": 285, "medical_critical": 43},
                "eta_critical": "34 min",
                "threat_description": "Market bridge inundation expected in 27m; rapid river rise +51cm/10m.",
                "safe_route": "Route B → Shelter-02 (Community Sports Complex)",
                "ndrf_team_assigned": "NDRF Unit-02 (Rishikesh Battalion)",
                "action_required": "Immediate Evacuation Order"
            },
            {
                "rank": 2,
                "village": "Village D (Sector D3 Valley Confluence)",
                "risk_score": max(70, int(current_risk - 4)),
                "risk_badge": "🔴 CRITICAL",
                "exposed_population": 1820,
                "vulnerable_groups": {"children": 310, "elderly": 195, "medical_critical": 28},
                "eta_critical": "29 min",
                "threat_description": "Lower valley stream convergence causing backwater flooding.",
                "safe_route": "Route South Ridge → High School Grounds",
                "ndrf_team_assigned": "NDRF Unit-04 (Quick Response Team)",
                "action_required": "Immediate Evacuation Order"
            },
            {
                "rank": 3,
                "village": "Village A (Upper Ridge / Sector A2)",
                "risk_score": max(45, int(current_risk - 15)),
                "risk_badge": "🟠 HIGH",
                "exposed_population": 3100,
                "vulnerable_groups": {"children": 520, "elderly": 340, "medical_critical": 52},
                "eta_critical": "1h 12m",
                "threat_description": "Steep slope runoff accumulation along minor seasonal ravines.",
                "safe_route": "East Hilltop Link → Temple Ridge Shelter",
                "ndrf_team_assigned": "State Disaster Response Force (SDRF)",
                "action_required": "Prepare Evacuation / Stage Buses"
            },
            {
                "rank": 4,
                "village": "Village C (Sector C1 Forest Flank)",
                "risk_score": max(35, int(current_risk - 32)),
                "risk_badge": "🟡 MODERATE",
                "exposed_population": 1070,
                "vulnerable_groups": {"children": 180, "elderly": 110, "medical_critical": 12},
                "eta_critical": "2h 30m",
                "threat_description": "Elevated terrace, monitoring riverbank embankment erosion.",
                "safe_route": "Main Highway North",
                "ndrf_team_assigned": "Local Volunteers & Police Post",
                "action_required": "Active Monitoring"
            }
        ]
        return villages

    def generate_multilingual_alert(self, level: int = 3, target_zone: str = "Zone B (Village B)") -> Dict[str, Any]:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S IST")
        
        alerts = {
            "en": {
                "language": "English",
                "title": "🔴 CRITICAL FLASH FLOOD WARNING - IMMEDIATE EVACUATION",
                "message": f"FLASH FLOOD EMERGENCY for {target_zone}. River is rising rapidly. Evacuate immediately via Route B towards Shelter-02 (Community Sports Complex). Avoid Riverside Road-1 and Bridge. Do not attempt to cross moving water.",
                "broadcast_channels": ["SMS Cell Broadcast", "WhatsApp Community Alert", "VHF Radio", "Loudspeaker Siren"]
            },
            "hi": {
                "language": "हिंदी (Hindi)",
                "title": "🔴 आकस्मिक बाढ़ की गंभीर चेतावनी - तत्काल खाली करें",
                "message": f"{target_zone} के लिए फ्लैश फ्लड आपातकाल! नदी का जलस्तर तेजी से बढ़ रहा है। तुरंत मार्ग-बी (Route B) से शेल्टर-02 (सामुदायिक खेल परिसर) की ओर सुरक्षित निकलें। नदी के किनारे वाली सड़क और पुल पर न जाएं। बहते पानी में गाड़ी न चलाएं।",
                "broadcast_channels": ["एसएमएस", "व्हाट्सएप", "लाउडस्पीकर सायरन", "रेडियो"]
            },
            "te": {
                "language": "తెలుగు (Telugu)",
                "title": "🔴 అత్యవసర మెరుపు వరద హెచ్చరిక - వెంటనే ఖాళీ చేయండి",
                "message": f"{target_zone} లో ఆకస్మిక వరద ముప్పు తీవ్రంగా ఉంది. వెంటనే రూట్-బి ద్వారా షెల్టర్-02 కి తరలి వెళ్లండి. నది వైపు వెళ్లే రోడ్డు మరియు వంతెనను ఉపయోగించవద్దు.",
                "broadcast_channels": ["SMS", "WhatsApp", "సైరన్"]
            },
            "kn": {
                "language": "ಕನ್ನಡ (Kannada)",
                "title": "🔴 ತುರ್ತು ಪ್ರವಾಹ ಎಚ್ಚರಿಕೆ - ತಕ್ಷಣವೇ ಸ್ಥಳಾಂತರಿಸಿ",
                "message": f"{target_zone} ಪ್ರದೇಶದಲ್ಲಿ ದಿಢೀರ್ ಪ್ರವಾಹ ಅಪಾಯ. ರೂಟ್-ಬಿ ಮೂಲಕ ಶೆಲ್ಟರ್-02 ಕಡೆಗೆ ತಕ್ಷಣವೇ ತೆರಳಿ. ನದಿಯ ಹತ್ತಿರವಿರುವ ರಸ್ತೆಯನ್ನು ಬಳಸಬೇಡಿ.",
                "broadcast_channels": ["SMS", "WhatsApp", "ಸೈರನ್"]
            },
            "ta": {
                "language": "தமிழ் (Tamil)",
                "title": "🔴 அவசர திடீர் வெள்ள எச்சரிக்கை - உடனே வெளியேறவும்",
                "message": f"{target_zone} பகுதியில் திடீர் வெள்ள அபாயம் ஏற்பட்டுள்ளது. உடனடியாக வழி-B வழியாக பாதுகாப்பான தங்குமிடம்-02க்கு செல்லவும். ஆற்றங்கரை சாலையை தவிர்க்கவும்.",
                "broadcast_channels": ["SMS", "WhatsApp", "ஒலிபெருக்கி"]
            }
        }

        record = {
            "id": f"ALERT-{len(self.alert_history) + 1:04d}",
            "timestamp": timestamp,
            "level": level,
            "target_zone": target_zone,
            "translations": alerts,
            "simulated_recipients_reached": 1843,
            "status": "BROADCAST_COMPLETED"
        }
        self.alert_history.insert(0, record)
        return record

    def get_alert_history(self) -> List[Dict[str, Any]]:
        return self.alert_history
