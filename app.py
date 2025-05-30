from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "6952a329fc685941264fa64652cec00b"

def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

def get_coordinates(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url).json()
    if response:
        lat = response[0]["lat"]
        lon = response[0]["lon"]
        name = response[0]["name"]
        country = response[0]["country"]
        return lat, lon, f"{name}, {country}"
    return None, None, None
def unix_to_time(timestamp, timezone_offset):
    return datetime.utcfromtimestamp(timestamp + timezone_offset).strftime('%H:%M')

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            lat, lon, location = get_coordinates(city)
            if lat and lon:
                url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
                response = requests.get(url).json()

                if response.get("cod") == "200":
                    sunrise = datetime.fromtimestamp(response["city"]["sunrise"])
                    sunset = datetime.fromtimestamp(response["city"]["sunset"])

                    forecast_list = []
                    for i in range(0, len(response["list"]), 8):
                        entry = response["list"][i]
                        forecast = {
                            "date": datetime.fromtimestamp(entry["dt"]).strftime("%a, %d %b"),
                            "temp": kelvin_to_celsius(entry["main"]["temp"]),
                            "humidity": entry["main"]["humidity"],
                            "wind": entry["wind"]["speed"],
                            "description": entry["weather"][0]["description"].title(),
                            "icon": entry["weather"][0]["icon"]
                        }
                        forecast_list.append(forecast)

                    weather_data = {
                        "city": location,
                        "sunrise": sunrise.strftime("%H:%M"),
                        "sunset": sunset.strftime("%H:%M"),
                        "forecast": forecast_list
                    }

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
