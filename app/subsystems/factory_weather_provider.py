# app/subsystems/factory_weather_provider.py
from abc import ABC, abstractmethod
from app.subsystems.current_weather_api import CurrentWeatherAPI
from app.subsystems.forecast_api import ForecastAPI
from app.subsystems.climate_api import ClimateAPI

# -------------------------------
# PRODUCT INTERFACE
# -------------------------------
class WeatherProvider(ABC):
    @abstractmethod
    def get_current_weather(self, lat, lon):
        pass

    @abstractmethod
    def get_forecast(self, lat, lon):
        pass

    @abstractmethod
    def get_climate(self, lat, lon, days):
        pass

# -------------------------------
# CONCRETE PRODUCT (OpenWeather Provider)
# -------------------------------
class OpenWeatherProvider(WeatherProvider):
    def __init__(self):
        self.current_api = CurrentWeatherAPI()
        self.forecast_api = ForecastAPI()
        self.climate_api = ClimateAPI()

    def get_current_weather(self, lat, lon):
        return self.current_api.get_weather(lat, lon)

    def get_forecast(self, lat, lon):
        return self.forecast_api.get_forecast(lat, lon)

    def get_climate(self, lat, lon, days):
        return self.climate_api.get_climate(lat, lon, days)

# -------------------------------
# CREATOR (Factory)
# -------------------------------
class WeatherProviderFactory(ABC):

    @abstractmethod
    def create_provider(self) -> WeatherProvider:
        pass

# -------------------------------
# CONCRETE CREATOR
# -------------------------------
class OpenWeatherFactory(WeatherProviderFactory):

    def create_provider(self) -> WeatherProvider:
        return OpenWeatherProvider()   # return concrete product
