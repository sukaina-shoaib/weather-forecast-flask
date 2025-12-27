import requests

class ForecastAPI:
    API_KEY = "b5307f7cd0b20101e16d0925b7a8d9b6"
    BASE_URL = "https://api.openweathermap.org/data/2.5"  # remove the space
    def get_forecast(self, lat, lon):
        url = f"{self.BASE_URL}/forecast"
        try:
            resp = requests.get(
                url,
                params={"lat": lat, "lon": lon, "appid": self.API_KEY, "units": "metric"},
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print("[FORECAST-ERROR]", e)
            return []          # safe empty list

        forecast_list = []
        for item in data["list"]:
            forecast_list.append({
                "time": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "condition": item["weather"][0]["description"]
            })
        return forecast_list