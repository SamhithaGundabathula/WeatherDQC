import json, os
from glob import glob
from datetime import datetime, timezone
import pandas as pd

def latest_file(pattern: str) -> str:
    files = sorted(glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files found matching: {pattern}")
    return files[-1]

def g(d, path, default=None):
    cur = d
    for key in path:
        if isinstance(key, int):
            if isinstance(cur, list) and len(cur) > key:
                cur = cur[key]
            else:
                return default
        else:
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return default
    return cur

raw_path = latest_file("data/raw/weather_nb_*.json")

with open(raw_path, "r", encoding="utf-8") as f:
    payload = json.load(f)

rows = []
for item in payload:
    d = item.get("data", {})
    if item.get("status") != 200 or d.get("cod") not in (200, "200"):
        rows.append({
            "city": None,
            "country": None,
            "observed_at_utc": None,
            "temp_c": None,
            "humidity_pct": None,
            "pressure_hpa": None,
            "wind_speed_mps": None,
            "weather_main": None,
            "weather_desc": None,
            "status": item.get("status"),
            "error": str(d.get("message")),
            "source_file": os.path.basename(raw_path),
            "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        continue

    dt_unix = d.get("dt")
    observed_at_utc = (
        datetime.fromtimestamp(dt_unix, tz=timezone.utc).isoformat()
        if isinstance(dt_unix, (int, float))
        else None
    )

    rows.append({
        "city": d.get("name"),
        "country": g(d, ["sys", "country"]),
        "observed_at_utc": observed_at_utc,
        "temp_c": g(d, ["main", "temp"]),
        "humidity_pct": g(d, ["main", "humidity"]),
        "pressure_hpa": g(d, ["main", "pressure"]),
        "wind_speed_mps": g(d, ["wind", "speed"]),
        "weather_main": g(d, ["weather", 0, "main"]),
        "weather_desc": g(d, ["weather", 0, "description"]),
        "status": 200,
        "error": None,
        "source_file": os.path.basename(raw_path),
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
    })

os.makedirs("data/processed", exist_ok=True)
out_csv = "data/processed/weather_nb_clean.csv"
pd.DataFrame(rows).to_csv(out_csv, index=False)

print("Read :", raw_path)
print("Saved:", out_csv)
print("Rows :", len(rows))
