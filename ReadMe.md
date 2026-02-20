# Description


Bulit a Data Engineering pipeline that collects live weather data, stores it, checks quality, and reports issues automatically.
## What the pipeline does

### Ingests data
Pulls live weather data from OpenWeatherMap API.

### Processes data
Cleans and flattens raw JSON into a structured format.

### Stores data
Loads cleaned data into PostgreSQL tables.

### Validates data quality
Checks for:

1.missing values

2.invalid ranges

3.duplicates

4.freshness (today’s data)

### Generates reports
Creates a daily DQ report (JSON/HTML) showing pass/fail status.

### Automates everything
Uses Apache Airflow to run the pipeline on a schedule.

### Runs in containers
Entire system runs using Docker (reproducible, portable).
