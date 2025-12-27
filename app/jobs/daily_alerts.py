#!/usr/bin/env python
import os, sys, traceback, logging, schedule, time
from app import create_app
from app.service.favorite_city_service import FavoriteCityService
from app.service.alert_service        import AlertService
from app.facade.weather_facade        import WeatherFacade
from app.service.user_service         import UserService

# ------------------------------------------------------------------
# 1.  push Flask context so Flask-Mail works outside request cycle
# ------------------------------------------------------------------
app = create_app()
app.app_context().push()

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s  %(message)s")

facade = WeatherFacade()
alert_service = AlertService()

def check_favourites():
    try:
        for user in UserService.get_all_users():
            uid = user["id"]
            print(f"[CRON] user {uid} -------------------")
            favourites = FavoriteCityService.get_user_favorites(uid)
            print(f"[CRON] favourites: {favourites}")
            for fav in favourites:
                city = fav["name"]
                print(f"[CRON] checking {city} ...")
                current = facade.get_current_weather(city)
                print(f"[CRON] temp in {city}: {current['temperature']}°C")
                alert_service.check_and_trigger_alerts(uid, city, current)
    except Exception as e:
        print("[CRON] crashed:", traceback.format_exc())# ------------------------------------------------------------------
# 2.  run every 5 min (change to .hour or .day.at("07:00") later)
# ------------------------------------------------------------------
schedule.every(1).seconds.do(check_favourites)
check_favourites()          # ← runs once immediately at start-up


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] %(levelname)s  %(message)s")
    logging.info("starting cron …")
    while True:
        schedule.run_pending()
        time.sleep(1)