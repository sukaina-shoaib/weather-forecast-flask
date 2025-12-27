import os
import requests
from typing import List, Dict, Any, Tuple

class ClimateAPI:
    BASE_URL = "https://pro.openweathermap.org/data/2.5/forecast/climate"
    API_KEY = os.getenv("OWM_KEY") or "be68c7a9354e94aeb4035cc27df31c18"

    def get_climate(self, lat: float, lon: float, days: int = 30) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Return (country_code, climate_list) for 1-30 days.
        Shape kept compatible with old stub.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "cnt": max(1, min(days, 30)),
            "appid": self.API_KEY,
            "units": "metric"
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            print("[CLIMATE-ERROR]", exc)
            return "", []          # safe empty tuple

        country = data["city"]["country"]          # ISO-2 code
        climate_list = []
        for day in data["list"]:
            climate_list.append({
                "date": day["dt"],
                "temp_day": day["temp"]["day"],
                "temp_min": day["temp"]["min"],
                "temp_max": day["temp"]["max"],
                "humidity": day["humidity"],
                "condition": day["weather"][0]["main"]
            })
        return country, climate_list