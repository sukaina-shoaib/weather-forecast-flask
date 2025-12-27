import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------- one-time retry adapter ----------
retry   = Retry(total=2, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session = requests.Session()
session.mount("https://", adapter)
# ----------------------------------
class GeocodingService:
    API_KEY = "be68c7a9354e94aeb4035cc27df31c18"

    def get_coordinates(self, city_name):
        url = "https://api.openweathermap.org/geo/1.0/direct"
        try:
            resp = requests.get(
                url,
                params={"q": city_name, "limit": 1, "appid": self.API_KEY},
                timeout=5
            )
            resp.raise_for_status()   # raises for 4xx/5xx
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print("[GEO-ERROR]", e)
            raise ValueError("City not found or service unreachable") from e

        if not data:
            raise ValueError("City not found")
        return data[0]["lat"], data[0]["lon"]