# transform_weather.py
# Reads the latest raw OpenWeather JSON in data/raw/ and writes a clean CSV to data/processed/

import json
import os
from glob import glob
from datetime import datetime, timezone

import pandas as pd


def latest_file(pattern: str) -> str:
    files = sorted(glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files found matching: {pattern}")
    return files[-1]


def safe_get(dct, path, default=None):
    cur = dct
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


# 1) pick latest raw json
raw_path = latest_file("data/raw/weather_*.json")

# 2) load json
with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 3) REQUIRED fields (core)
dt_unix = data.get("dt")  # seconds since epoch
observed_at_utc = (
    datetime.fromtimestamp(dt_unix, tz=timezone.utc).isoformat()
    if isinstance(dt_unix, (int, float))
    else None
)

row = {
    # identity/time
    "city": data.get("name"),
    "country": safe_get(data, ["sys", "country"]),
    "observed_at_utc": observed_at_utc,
    "observed_at_unix": dt_unix,
    # main weather metrics
    "temp_c": safe_get(data, ["main", "temp"]),
    "feels_like_c": safe_get(data, ["main", "feels_like"]),
    "humidity_pct": safe_get(data, ["main", "humidity"]),
    "pressure_hpa": safe_get(data, ["main", "pressure"]),
    # wind + condition
    "wind_speed_mps": safe_get(data, ["wind", "speed"]),
    "weather_main": safe_get(data, ["weather", 0, "main"]),
    "weather_desc": safe_get(data, ["weather", 0, "description"]),
    # run metadata (helpful later)
    "source_file": os.path.basename(raw_path),
    "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
}

# 4) write csv
os.makedirs("data/processed", exist_ok=True)
out_csv = "data/processed/weather_clean.csv"
pd.DataFrame([row]).to_csv(out_csv, index=False)

print("Read :", raw_path)
print("Saved:", out_csv)
