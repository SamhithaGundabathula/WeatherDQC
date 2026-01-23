import json
import requests
from datetime import datetime

API_KEY = "260ca98e3c6f4a013a97568554bfd03a"
url = f"https://api.openweathermap.org/data/2.5/weather?zip=E3A,ca&units=metric&appid={API_KEY}"

data = requests.get(url).json()

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"data/raw/weather_E3A_{ts}.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved:", out_path)
