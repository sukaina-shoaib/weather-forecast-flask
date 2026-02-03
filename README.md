# Weather Forecasting Website


## Live Website

 **[https://sukaina.pythonanywhere.com/login](https://sukaina.pythonanywhere.com/login)**

---

##  Project Description

The **Weather Forecasting Website** is a web-based application that provides **real-time weather updates**, forecasts, and personalized alerts through a **simple and user-friendly interface**.
The system allows users to search weather by city, track multiple locations, and receive alerts based on specific weather conditions.

This project applies **software engineering principles**, **design patterns**, and **real-time API integration** as part of a Final Year Project.

---

##  Problem Statement

Most existing weather applications:

* Are complex and difficult to use
* Lack personalization
* Do not support multi-city tracking
* Do not provide user-defined weather alerts

Users need a **simple, customizable, and reliable** platform for weather forecasting.

---

##  Solution

This project solves the problem by offering:

* Real-time weather data using reliable APIs
* Personalized dashboards
* Multi-city weather tracking
* Custom alerts for temperature, rain, wind, and storms
* Clean and responsive UI


## Features

* User signup and login
* City-based weather search
* Real-time weather conditions
* 7-day weather forecast
* Save and manage favorite cities
* Personalized weather alerts
* Email / dashboard notifications
* Responsive design (desktop & mobile)

## Design Patterns Used

###  Factory Method Pattern

* Used to create weather data objects
* Allows switching between multiple weather APIs
* Improves flexibility and scalability

###  Observer Pattern

* Used for weather alerts
* Users subscribe to weather updates
* Notifications are sent automatically when conditions change

###  Facade Pattern

* Simplifies complex backend operations
* Hides API calls, data processing, and alert logic behind a simple interface

### Related Pattern Diagrams:-
<img width="1380" height="774" alt="image" src="https://github.com/user-attachments/assets/80c83e9b-c193-4eca-816c-695249c83aac" />
<img width="1131" height="766" alt="image" src="https://github.com/user-attachments/assets/affb9143-0eb1-46c9-8041-2bd8fdd4e4ab" />


##  System Architecture

* **Architecture:** MVC (Model–View–Controller)
* **Frontend:** HTML, CSS, Bootstrap
* **Backend:** Flask (Python)
* **Database:** MySQL
* **APIs:** OpenWeather API / WeatherAPI
* **Notifications:** Email & dashboard alerts

---

##  Technologies Used

### Languages & Frameworks

* Python
* Flask
* HTML, CSS, Bootstrap

### Libraries & Tools

* Requests
* SQLAlchemy
* Chart.js
* Flask-Mail / SMTP
* Weather API SDKs

---

## How It Works

1. User logs in or registers
2. Enters a city name
3. System fetches live weather data
4. Weather details and forecast are displayed
5. Alerts are triggered if user-defined conditions are met

##  Future Enhancements

* Mobile application
* AI-based weather prediction
* Push notifications
* Improved UI/UX
* Performance optimization

---

## References

* OpenWeather API Documentation
* WeatherAPI Developer Docs
* *Design Patterns: Elements of Reusable Object-Oriented Software*
* Flask Official Documentation
* MDN Web Docs & W3Schools

---

## Conclusion

The **Weather Forecasting Website** successfully delivers a **simple, accurate, and personalized weather forecasting solution**.



