from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

def unix_to_time(timestamp, timezone_offset):
    return datetime.utcfromtimestamp(timestamp + timezone_offset).strftime('%H:%M')

def get_weather_data(city):
    API_KEY = os.getenv("OPENWEATHER_API_KEY") or "6952a329fc685941264fa64652cec00b"

    # 1. Get coordinates via Geocoding API
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_data = requests.get(geo_url).json()
    if not geo_data:
        return None

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

    # 2. Get current weather for sunrise/sunset
    current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    current_data = requests.get(current_url).json()
    timezone_offset = current_data.get("timezone", 0)
    sunrise = unix_to_time(current_data["sys"]["sunrise"], timezone_offset)
    sunset = unix_to_time(current_data["sys"]["sunset"], timezone_offset)

    # 3. Get 5-day forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    forecast_data = requests.get(forecast_url).json()
    forecast_list = forecast_data["list"]
    daily = []
    used_dates = set()

    for item in forecast_list:
        date_only = item["dt_txt"].split(" ")[0]
        if date_only in used_dates:
            continue
        used_dates.add(date_only)

        daily.append({
            "date": date_only,
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"].title(),
            "icon": item["weather"][0]["icon"],
            "humidity": item["main"]["humidity"],
            "wind": item["wind"]["speed"]
        })

        if len(daily) == 5:
            break

    return {
        "city": current_data["name"],
        "sunrise": sunrise,
        "sunset": sunset,
        "forecast": daily
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        weather = get_weather_data(city)
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
