# app/services/weather_service.py
from app.facade.weather_facade import WeatherFacade
from app.service.city_service import CityService
from app.service.weather_log_service import WeatherLogService

class WeatherService:

    def __init__(self):
        self.facade = WeatherFacade()

    def get_or_create_city(self, city_name):
        """Find city or add if missing"""
        city = CityService.get_city_by_name(city_name)
        if city:
            return city  # dictionary with id, name, country

        city_id = CityService.add_city(city_name)
        return {"id": city_id, "name": city_name}

    def get_current_weather(self, city_name):
        city = self.get_or_create_city(city_name)

        weather = self.facade.get_current_weather(city_name)

        WeatherLogService.save_weather_log(
            city_id=city["id"],
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            wind_speed=weather["wind_speed"],
            condition=weather["condition"],
        )

        return weather

    def get_forecast(self, city_name):
        self.get_or_create_city(city_name)
        return self.facade.get_forecast(city_name)
