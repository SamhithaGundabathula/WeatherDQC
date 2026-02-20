# Weather Data Quality Pipeline

An end-to-end Data Engineering pipeline that ingests live weather data from OpenWeatherMap, loads it into PostgreSQL, validates data quality, orchestrates workflows with Airflow, and exposes a web-based DQ dashboard.

---

## Architecture Overview

```
OpenWeatherMap API → Extract (Python) → Transform (Normalize JSON) → Load (PostgreSQL in Docker) → Data Quality Checks → Airflow Orchestration → Streamlit Dashboard
```

---

## Tech Stack

- Python
- PostgreSQL (Dockerized)
- SQLAlchemy + Psycopg2
- Apache Airflow (LocalExecutor)
- Streamlit (Web Dashboard)
- Docker & Docker Compose

---

## Project Structure

```
weatherDQC/
│
├── data/
│   ├── raw/
│   └── processed/
│── steps/
│   ├── Dashboardimage
│   └── HowToRun.md
│	└── envSetup.md
│   
│
├── dags/
│   └── weather_nb_pipeline.py
│
├── extract_weather.py
├── transform_weather.py
├── load_nb_to_postgres.py
├── run_dq_and_report.py
├── dq_dashboard.py
│
├── Dockerfile.dashboard
├── docker-compose.yml
└── README.md
```

---

## Features Implemented

### 1. Data Ingestion

- Pulls live weather data from OpenWeatherMap API
- Extracts multiple NB cities
- Stores raw JSON files with timestamped filenames

### 2. Transformation

- Normalizes nested JSON
- Converts temperature to Celsius
- Extracts:
  - `city`
  - `observed_at_utc`
  - `temp_c`
  - `humidity_pct`
  - `pressure_hpa`
  - `wind_speed`
  - `cloud_pct`
  - `ingested_at_utc`

### 3. Load (PostgreSQL in Docker)

- Uses SQLAlchemy
- Appends daily data
- Proper timestamp handling (UTC)

### 4. Data Quality Checks

Automated checks stored in `dq_results`:

- Null checks (temp, humidity, pressure)
- Range validation
- Duplicate detection (city + timestamp)
- Freshness check (today's data exists)

Each run generates:

- DQ audit table entry
- JSON report file

---

## Airflow Orchestration

**DAG:** `weather_nb_daily_pipeline`

**Task order:**

```
extract → transform → load → dq
```

- Runs daily
- Handles retries
- Tracks run history in Airflow metadata DB
- Uses Postgres backend (not SQLite)

---

## Web Dashboard

Streamlit dashboard running inside Docker.

**Shows:**

- Latest Run ID
- Passed / Failed checks
- Failure details
- Historical DQ results

**Access:**

```
http://localhost:8501
```

---

## Docker Setup

**Services:**

- `postgres`
- `pgadmin`
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-init`
- `dq-dashboard`

**Start everything:**

```bash
docker compose up -d --build
```

**Stop:**

```bash
docker compose down
```

---

## Database Tables

### `weather_nb`
Stores processed weather data (historical).

### `dq_results`
Stores data quality audit results.

---

## Key Learning Outcomes

- Built full ETL pipeline from scratch
- Understood Docker networking (service name vs localhost)
- Implemented production-style data quality validation
- Designed Airflow DAG with LocalExecutor + Postgres backend
- Built internal web dashboard for pipeline monitoring
- Debugged containerized environment issues (paths, networking, executors)

---

## Future Improvements

- Add unique constraint on `(city, observed_at_utc)`
- Add incremental loading logic
- Add Slack/email alerts on failure
- Add daily aggregation table
- Deploy to cloud (AWS ECS / EC2)

---

