from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="weather_nb_daily_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 1},
    tags=["weather", "etl", "dq"],
) as dag:

  extract = BashOperator(
    task_id="extract_nb_weather",
    bash_command="cd /opt/airflow/project && python extract_weather.py",
)

transform = BashOperator(
    task_id="transform_nb_weather",
    bash_command="cd /opt/airflow/project && python transform_weather.py",
)

load = BashOperator(
    task_id="load_to_postgres",
    bash_command="cd /opt/airflow/project && python load_nb_to_postgres.py",
)

dq = BashOperator(
    task_id="run_dq_and_report",
    bash_command="cd /opt/airflow/project && python run_dq_and_report.py",
)


extract >> transform >> load >> dq
