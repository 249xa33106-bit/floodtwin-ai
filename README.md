# FLOODTWIN AI ??
### AI-Powered Hyper-Local Flash Flood Prediction, Digital Twin & Dynamic Evacuation Decision Support System

> Built for the National Disaster Response Force (NDRF) and District Disaster Management Authorities.

---

## ?? Core System Highlights

1. **Hyper-Local 250m × 250m Resolution**: Predictions are computed per $250\text{m} \times 250\text{m}$ grid cell rather than district-wide generalizations.
2. **Multi-Source Data Fusion**: Real-time sliding rainfall accumulation ($30\text{m}, 1\text{h}, 3\text{h}, 6\text{h}, 12\text{h}, 24\text{h}$, forecast $1\text{h}/3\text{h}$), river water level rise velocity ($+51\text{ cm}/10\text{min}$) & acceleration, SRTM 30m DEM elevation, and IoT sensors.
3. **Hybrid AI & Explainable SHAP Attribution**: Blends XGBoost Machine Learning with a Deterministic Hydrological Safety Model and breaks down *why* risk is critical (e.g. Extreme Rainfall $+29\%$, Rapid River Rise $+23\%$, Soil Saturation $+19\%$, Steep Upstream Terrain $+16\%$).
4. **4D Future Flood Twin (NOW ? +120 MIN)**: 2D Cellular Automata simulation displaying water depth expansion across time steps with Copernicus Sentinel-1 SAR satellite validation overlay.
5. **Dynamic Evacuation Routing**: Flood-aware A* / Dijkstra router checking road submersion times vs. travel times to avoid drowning traps and routing to high-ground shelters.
6. **Sensor Trust & Anomaly Detection**: Automatic spike detection and trust degradation to protect against sensor hardware malfunctions.
7. **NDRF Grounded Incident Commander & Multilingual Siren Alerts**: Context-aware tactical assistant responding to operational directives and broadcasting alerts in 6 languages.

---

## ?? Quickstart Guide

### 1. Backend (FastAPI + XGBoost + SHAP)
```bash
# From repository root:
pip install -r backend/requirements.txt
python backend/main.py
# Backend runs at http://127.0.0.1:8000
```

### 2. Frontend (React + Tailwind + Leaflet)
```bash
# From repository root:
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:3000
```

---

## ?? Testing
```bash
python -m pytest backend/test_backend.py -v
```
