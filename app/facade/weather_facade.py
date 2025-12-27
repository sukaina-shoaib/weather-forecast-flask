# app/facade/weather_facade.py

from app.subsystems.geocoding_service import GeocodingService
from app.subsystems.factory_weather_provider import OpenWeatherFactory

# facade complier
class WeatherFacade:

    def __init__(self):
        self.geo = GeocodingService()
        self.factory = OpenWeatherFactory()
        self.provider = self.factory.create_provider()  # Factory Method used here!

    def get_current_weather(self, city_name):
        lat, lon = self.geo.get_coordinates(city_name)
        return self.provider.get_current_weather(lat, lon)

    def get_7day_forecast(self, city_name):
        lat, lon = self.geo.get_coordinates(city_name)
        return self.provider.get_forecast(lat, lon)

    def get_30day_climate(self, city_name, days=30):
        lat, lon = self.geo.get_coordinates(city_name)
        return self.provider.get_climate(lat, lon, days)
