import requests, json, os
from datetime import datetime
from config import API_KEY, BASE_URL

DATA_FILE = os.path.join("data", "weather.json")

def get_location_from_ip():
    """Get user's city based on their IP address"""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return data["city"]
        else:
            return None
    except Exception as e:
        print("Error fetching location:", e)
        return None


def get_weather(city=None):
    """Fetch current weather for a city (or detect live location)."""
    if not city or city.strip() == "":
        city = get_location_from_ip()
        if not city:
            city = "London"  # fallback if location not found

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["main"]
            }
        else:
            return None
    except Exception as e:
        print("Error fetching weather:", e)
        return None


def get_outfit_suggestion(weather):
    """Simple rule-based outfit logic."""
    temp = weather["temp"]
    condition = weather["condition"].lower()

    if "rain" in condition: 
        outfit = "Take an umbrella ☔ and wear a raincoat." 
    elif temp < 10 and temp > 5: 
        outfit = "Heavy jacket + gloves 🧤." 
    elif temp > 30 and temp < 35: 
        outfit = "Wear light clothes 👕 and sunglasses 🕶️." 
    elif temp > 35: 
        outfit = "Very hot! Wear shorts 🩳, light clothes 🎽 and drink water 💧." 
    elif 15 <= temp <= 30: 
        outfit = "A T-shirt 👚 and jeans 👖 are fine." 
    elif "snow" in condition: 
        outfit = "Winter coat ☃️, scarf 🧣, boots 👢." 
    else: 
        outfit = "Wear warm clothes 🧥, maybe a sweater."

    save_history(weather, outfit)
    return outfit


def save_history(weather, outfit):
    """Append query result to data/weather.json"""
    entry = {
        "city": weather["city"],
        "temp": weather["temp"],
        "condition": weather["condition"],
        "outfit": outfit,
        "timestamp": datetime.now().isoformat()
    }

    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    history.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)
