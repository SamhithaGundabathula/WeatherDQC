
# Data Source

**API**: 
OpenWeatherMap – Current Weather Data API

**Format**: JSON

**Data Type**: Real-time weather observations

**Units**: Metric (°C)

# Pipeline Architecture (Current Progress)
## Data Ingestion (Extract)

1. Integrated with OpenWeatherMap API to retrieve live weather data

2. Implemented a Python-based extraction script using requests

3. Stored raw API responses as timestamped JSON files to maintain data lineage and enable reprocessing

## Data Processing (Transform)

1. Safely parsed nested JSON structures

2. Selected and standardized key weather attributes (temperature, humidity, pressure, wind speed, conditions)

3. Converted Unix timestamps to UTC datetime

4. Flattened data into a structured tabular format

5. Persisted cleaned data as CSV for downstream loading

## Containerized Database Infrastructure

1. Deployed PostgreSQL using Docker Compose

2. Configured pgAdmin for database inspection and management

3. Implemented persistent Docker volumes to ensure data durability across container restarts

4. Verified connectivity using containerized psql and project-scoped pgcli

## Development Environment

1. Managed dependencies using a project-scoped Python virtual environment (uv)

2. Ensured tool isolation to avoid global dependency conflicts

Followed a phased workflow: local development → validation → containerization

# Technology Stack

Programming Language: Python

API Integration: OpenWeatherMap

Database: PostgreSQL

Containers: Docker, Docker Compose

Data Processing: pandas

Tooling: pgAdmin, pgcli

