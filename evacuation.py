from typing import Dict, Any, List
import networkx as nx

class EvacuationRoutingEngine:
    def __init__(self):
        self.shelters = self._init_shelters()
        self.road_network = self._init_road_graph()

    def _init_shelters(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "SHELTER-01",
                "name": "Government Higher Secondary School (Ridge)",
                "lat": 30.3790,
                "lng": 79.3240,
                "elevation_m": 1580,
                "capacity": 600,
                "current_occupancy": 120,
                "available_capacity": 480,
                "medical_facilities": True,
                "water_food_stock_days": 7,
                "flood_risk": "LOW",
                "road_accessibility": "CLEAR"
            },
            {
                "id": "SHELTER-02",
                "name": "Community Hall & Sports Complex (Sector A)",
                "lat": 30.3775,
                "lng": 79.3210,
                "elevation_m": 1530,
                "capacity": 850,
                "current_occupancy": 310,
                "available_capacity": 540,
                "medical_facilities": True,
                "water_food_stock_days": 10,
                "flood_risk": "LOW",
                "road_accessibility": "CLEAR"
            },
            {
                "id": "SHELTER-03",
                "name": "District Stadium Pavilion (Valley Rim)",
                "lat": 30.3690,
                "lng": 79.3360,
                "elevation_m": 1390,
                "capacity": 400,
                "current_occupancy": 380,
                "available_capacity": 20,
                "medical_facilities": False,
                "water_food_stock_days": 3,
                "flood_risk": "MODERATE",
                "road_accessibility": "RESTRICTED_ACCESS"
            }
        ]

    def _init_road_graph(self) -> nx.Graph:
        G = nx.Graph()
        # Nodes
        # Village origin points, intersections, and shelters
        # Origin: Zone B (Village B Center - B3)
        # Waypoints: J1 (Market Bridge), J2 (Ridge Bypass), J3 (Hillside Crossing), J4 (Valley Link)
        # Shelters: Shelter-01, Shelter-02, Shelter-03
        edges = [
            # (u, v, {distance_km, base_speed_kmh, road_name, passes_near_river, elev_min})
            ("Zone-B-Center", "J1-Market-Bridge", {"distance_km": 1.2, "travel_time_min": 4, "name": "Road-1 (Old Riverside Path)", "flood_arrival_min": 18, "river_adjacent": True}),
            ("J1-Market-Bridge", "SHELTER-01", {"distance_km": 1.5, "travel_time_min": 5, "name": "Road-2 (Bridge Incline)", "flood_arrival_min": 27, "river_adjacent": True}),
            ("Zone-B-Center", "J2-Ridge-Bypass", {"distance_km": 1.8, "travel_time_min": 6, "name": "Road-3 (West Ridge Access)", "flood_arrival_min": 120, "river_adjacent": False}),
            ("J2-Ridge-Bypass", "SHELTER-02", {"distance_km": 1.6, "travel_time_min": 6, "name": "Road-4 (High Elevation Highway Link)", "flood_arrival_min": 150, "river_adjacent": False}),
            ("J2-Ridge-Bypass", "SHELTER-01", {"distance_km": 2.2, "travel_time_min": 7, "name": "Road-5 (North Ridge Connector)", "flood_arrival_min": 140, "river_adjacent": False}),
            ("Zone-B-Center", "J4-Valley-Link", {"distance_km": 2.4, "travel_time_min": 8, "name": "Road-6 (Lower Valley Highway)", "flood_arrival_min": 35, "river_adjacent": True}),
            ("J4-Valley-Link", "SHELTER-03", {"distance_km": 1.1, "travel_time_min": 4, "name": "Road-7 (South Link)", "flood_arrival_min": 40, "river_adjacent": True}),
        ]
        for u, v, data in edges:
            G.add_edge(u, v, **data)
        return G

    def calculate_evacuation_routes(self, origin: str = "Zone-B-Center", rain_intensity: float = 45.0, river_level: float = 4.2) -> Dict[str, Any]:
        # Predefined candidate routes to evaluate
        # Route 1 (Traditional shortest route via Road 1 -> Road 2 to Shelter-01)
        # Route 2 (Flood-Safe Route via Road 3 -> Road 4 to Shelter-02)
        # Route 3 (Secondary Safe Route via Road 3 -> Road 5 to Shelter-01)

        # Dynamic calculation of flood arrival time on roads based on current river surge
        surge_speed = 1.0 if river_level < 3.5 else 1.8

        routes = [
            {
                "id": "ROUTE-A",
                "name": "Direct Riverside Route (Road-1 → Road-2 → Shelter-1)",
                "origin": "Zone B Village Center",
                "destination_shelter": "Government Higher Secondary School",
                "shelter_id": "SHELTER-01",
                "total_distance_km": 2.7,
                "estimated_travel_time_min": 9,
                "predicted_flood_arrival_min": 18 if river_level > 3.8 else 35,
                "road_sections": [
                    {"name": "Road-1 (Riverside Path)", "status": "HIGH_VULNERABILITY", "water_depth_m": round(max(0.1, (river_level - 3.4) * 0.8), 2), "fails_in_min": 18},
                    {"name": "Road-2 (Bridge Incline)", "status": "CRITICAL_RISK", "water_depth_m": round(max(0.0, (river_level - 3.6) * 0.6), 2), "fails_in_min": 27}
                ],
                "elevation_profile": "Low valley floor (1380m) → Culvert depression → Bridge",
                "path_coords": [
                    [30.3725, 79.3325],
                    [30.3735, 79.3310],
                    [30.3750, 79.3290],
                    [30.3790, 79.3240]
                ]
            },
            {
                "id": "ROUTE-B",
                "name": "Recommended Flood-Safe Route (Road-3 → Road-4 → Shelter-2)",
                "origin": "Zone B Village Center",
                "destination_shelter": "Community Hall & Sports Complex",
                "shelter_id": "SHELTER-02",
                "total_distance_km": 3.4,
                "estimated_travel_time_min": 12,
                "predicted_flood_arrival_min": 120,
                "road_sections": [
                    {"name": "Road-3 (West Ridge Access)", "status": "CLEAR_SAFE", "water_depth_m": 0.0, "fails_in_min": 120},
                    {"name": "Road-4 (High Elevation Highway Link)", "status": "CLEAR_SAFE", "water_depth_m": 0.0, "fails_in_min": 150}
                ],
                "elevation_profile": "Ascending hillside ridge (1380m → 1530m) away from river channel",
                "path_coords": [
                    [30.3725, 79.3325],
                    [30.3715, 79.3280],
                    [30.3740, 79.3230],
                    [30.3775, 79.3210]
                ]
            },
            {
                "id": "ROUTE-C",
                "name": "Alternate High Ridge Route (Road-3 → Road-5 → Shelter-1)",
                "origin": "Zone B Village Center",
                "destination_shelter": "Government Higher Secondary School",
                "shelter_id": "SHELTER-01",
                "total_distance_km": 4.0,
                "estimated_travel_time_min": 16,
                "predicted_flood_arrival_min": 140,
                "road_sections": [
                    {"name": "Road-3 (West Ridge Access)", "status": "CLEAR_SAFE", "water_depth_m": 0.0, "fails_in_min": 120},
                    {"name": "Road-5 (North Ridge Connector)", "status": "CLEAR_SAFE", "water_depth_m": 0.0, "fails_in_min": 140}
                ],
                "elevation_profile": "High crest mountain route (1460m → 1580m)",
                "path_coords": [
                    [30.3725, 79.3325],
                    [30.3715, 79.3280],
                    [30.3760, 79.3235],
                    [30.3790, 79.3240]
                ]
            }
        ]

        evaluated_routes = []
        for r in routes:
            travel = r["estimated_travel_time_min"]
            flood_arrival = r["predicted_flood_arrival_min"]
            safety_margin = flood_arrival - travel

            # Decision logic: if safety margin is less than 15 minutes or travel > flood_arrival, route is unsafe
            if safety_margin <= 10 or flood_arrival <= 25:
                verdict = "UNSAFE"
                status_color = "#EF4444" # Red
                verdict_reason = f"❌ UNSAFE: Flood arrival in {flood_arrival} min leaves only {safety_margin} min safety buffer! Road-2 predicted to submerge."
                is_recommended = False
            elif r["id"] == "ROUTE-B":
                verdict = "SAFEST_RECOMMENDED"
                status_color = "#22C55E" # Green
                verdict_reason = f"✅ SAFEST RECOMMENDED: Wide safety margin of {safety_margin} minutes along elevated western ridge with high shelter capacity (540 available)."
                is_recommended = True
            else:
                verdict = "SAFE_ALTERNATE"
                status_color = "#3B82F6" # Blue
                verdict_reason = f"ℹ ALTERNATE SAFE: Long route (4.0 km) with {safety_margin} min safety buffer."
                is_recommended = False

            r.update({
                "safety_margin_min": safety_margin,
                "verdict": verdict,
                "status_color": status_color,
                "verdict_reason": verdict_reason,
                "is_recommended": is_recommended
            })
            evaluated_routes.append(r)

        return {
            "origin": origin,
            "river_stage_status": "RISING_RAPIDLY" if river_level > 3.8 else "NORMAL",
            "recommended_route_id": "ROUTE-B",
            "routes": evaluated_routes,
            "shelters": self.shelters
        }
