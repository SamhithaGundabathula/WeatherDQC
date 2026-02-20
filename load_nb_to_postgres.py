import os
import pandas as pd
from sqlalchemy import create_engine



CSV_PATH = "data/processed/weather_nb_clean.csv"

# Postgres running in Docker, exposed to your machine at localhost:5432
DB_USER = "root"
DB_PASS = "root"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "weatherdb"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_csv(CSV_PATH)

# Convert timestamps (so Postgres stores proper timestamptz)
if "observed_at_utc" in df.columns:
    df["observed_at_utc"] = pd.to_datetime(df["observed_at_utc"], errors="coerce", utc=True)
if "ingested_at_utc" in df.columns:
    df["ingested_at_utc"] = pd.to_datetime(df["ingested_at_utc"], errors="coerce", utc=True)

df.to_sql("weather_nb", engine, if_exists="append", index=False)

print(f"Loaded {len(df)} rows into weather_nb")
