import logging
from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'

    # Flask-Mail
    app.config['MAIL_SERVER']   = 'smtp.gmail.com'
    app.config['MAIL_PORT']     = 587
    app.config['MAIL_USE_TLS']  = True
    app.config['MAIL_USERNAME'] = 'weatherforecast151@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ycqq gvab dezp glly'  # 16-char app password
    mail.init_app(app)

    logging.basicConfig(level=logging.DEBUG)

    # ---------- import & register blueprints ----------
    from app.controllers.home_controller      import home_bp
    from app.controllers.auth_controller      import auth_bp
    from app.controllers.alerts_controller    import alerts_bp
    from app.controllers.favorites_controller import fav_bp
    from app.controllers.notification_controller import notif_bp
    from app.controllers.user_controller      import user_bp
    from app.controllers.api_controller       import api_bp
    from app.controllers.error_controller     import err_bp
    from app.controllers.weather_controller   import weather_bp

    for bp in (home_bp, auth_bp, alerts_bp, fav_bp, notif_bp,
               user_bp, api_bp, err_bp, weather_bp):
        app.register_blueprint(bp)

    # ---------- custom Jinja filter ----------
    def weather_icon(condition: str) -> str:
        c = condition.lower()
        if 'rain' in c:        return '🌧️'
        if 'snow' in c:        return '❄️'
        if 'thunderstorm' in c:return '⛈️'
        if 'drizzle' in c:     return '🌦️'
        if 'clear' in c:       return '☀️'
        if 'few clouds' in c:  return '🌤️'
        if 'scattered clouds' in c or 'broken clouds' in c: return '⛅'
        if 'overcast' in c or 'cloud' in c: return '☁️'
        if 'mist' in c or 'fog' in c:       return '🌫️'
        return '🌤️'          # fallback
    app.jinja_env.filters['icon'] = weather_icon

    return app