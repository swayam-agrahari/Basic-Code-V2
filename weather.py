import requests
import time
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict, Callable, Optional

# === CONFIGURATION ===

OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_email_password"
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "recipient_email@gmail.com"

DEFAULT_REMINDERS = {
    "rain": "Bring an umbrella! ☔",
    "snow": "Snow alert! Dress warmly and drive safely.",
    "clear": "It's a perfect day for outdoor activities!",
    "clouds": "Might want to bring a jacket, it's a bit chilly.",
    "hot": "Wear sunscreen! Stay cool.",
    "cold": "Dress warmly and bundle up!",
    "wind": "It's windy today! Hold onto your hat.",
    "humid": "Stay hydrated, it's a humid one today."
}

CUSTOM_REMINDERS: Dict[str, str] = {
    # Example: "pollen": "Take allergy medication!"
}

ConditionFunc = Callable[[dict], bool]

# === WEATHER CONDITIONS ===

def cond_rain(data: dict) -> bool:
    return any("rain" in w["main"].lower() or 500 <= w["id"] < 600 for w in data.get("weather", []))

def cond_snow(data: dict) -> bool:
    return any("snow" in w["main"].lower() or 600 <= w["id"] < 700 for w in data.get("weather", []))

def cond_clear(data: dict) -> bool:
    return any("clear" in w["main"].lower() for w in data.get("weather", []))

def cond_clouds(data: dict) -> bool:
    return any("cloud" in w["main"].lower() for w in data.get("weather", []))

def cond_hot(data: dict) -> bool:
    temp = data.get("main", {}).get("temp")
    return temp is not None and temp > 30.0

def cond_cold(data: dict) -> bool:
    temp = data.get("main", {}).get("temp")
    return temp is not None and temp < 10.0

def cond_wind(data: dict) -> bool:
    return data.get("wind", {}).get("speed", 0.0) > 8.0

def cond_humid(data: dict) -> bool:
    humidity = data.get("main", {}).get("humidity")
    return humidity is not None and humidity > 75

CONDITIONS: Dict[str, ConditionFunc] = {
    "rain": cond_rain,
    "snow": cond_snow,
    "clear": cond_clear,
    "clouds": cond_clouds,
    "hot": cond_hot,
    "cold": cond_cold,
    "wind": cond_wind,
    "humid": cond_humid
}

# === WEATHER DATA ===

def fetch_weather(city: str, units: str = "metric") -> Optional[dict]:
    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": units,
    }
    try:
        resp = requests.get(base, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")
        return None

def generate_reminders(weather_data: dict) -> List[str]:
    reminders = []
    for cond_key, func in CONDITIONS.items():
        if func(weather_data):
            msg = CUSTOM_REMINDERS.get(cond_key) or DEFAULT_REMINDERS.get(cond_key)
            if msg:
                reminders.append(msg)
    if not reminders:
        reminders.append("Be prepared for your day — weather is mild.")
    return reminders

def format_weather_summary(city: str, weather_data: dict) -> str:
    desc = ", ".join(w.get("description", "") for w in weather_data.get("weather", []))
    temp = weather_data.get("main", {}).get("temp")
    humidity = weather_data.get("main", {}).get("humidity")
    wind_speed = weather_data.get("wind", {}).get("speed")
    return (f"Weather in {city}: {desc}. "
            f"Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s.")

# === NOTIFICATION ===

def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

def notify(city: str, weather_data: dict):
    summary = format_weather_summary(city, weather_data)
    reminders = generate_reminders(weather_data)
    body = summary + "\n\nReminders:\n" + "\n".join(f"- {r}" for r in reminders)
    print(body)
    # send_email(f"Weather Reminder for {city}", body)

def check_for_cities(cities: List[str]):
    for city in cities:
        weather = fetch_weather(city)
        if weather:
            notify(city, weather)
        else:
            print(f"Could not get weather for {city}")

def schedule_periodic_check(cities: List[str], interval_minutes: int = 60):
    while True:
        print(f"=== Checking weather at {time.ctime()} ===")
        check_for_cities(cities)
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    cities_to_monitor = ["Thiruvananthapuram", "New York"]
    check_for_cities(cities_to_monitor)
    # schedule_periodic_check(cities_to_monitor, interval_minutes=60)
