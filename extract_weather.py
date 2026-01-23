import json
import requests
from datetime import datetime

import os
API_KEY = os.getenv("OPENWEATHER_API_KEY")
url = f"https://api.openweathermap.org/data/2.5/weather?zip=E3A,ca&units=metric&appid={API_KEY}"

data = requests.get(url).json()

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"data/raw/weather_E3A_{ts}.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved:", out_path)
