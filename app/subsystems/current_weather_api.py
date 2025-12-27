import requests

class CurrentWeatherAPI:
    API_KEY = "be68c7a9354e94aeb4035cc27df31c18"
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def get_weather(self, lat, lon):
        url = f"{self.BASE_URL}/weather"
        try:
            resp = requests.get(
                url,
                params={"lat": lat, "lon": lon, "appid": self.API_KEY, "units": "metric"},
                timeout=5
            )
            resp.raise_for_status()
            r = resp.json()
        except requests.exceptions.RequestException as e:
            print("[CURRENT-ERROR]", e)
            raise ValueError("Current-weather service unreachable") from e

        return {
            "temperature": r["main"]["temp"],
            "humidity": r["main"]["humidity"],
            "wind_speed": r["wind"]["speed"],
            "condition": r["weather"][0]["description"]
        }