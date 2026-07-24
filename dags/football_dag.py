from datetime import datetime, timedelta
import sys
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

# Agregamos la carpeta de scripts al path para poder importarlos
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from extract import extract_matches, save_raw_data
from transform import load_latest_raw_file, transform_matches
from load import load_to_postgres

COMPETITION_CODE = "WC"


def task_extract():
    data = extract_matches(COMPETITION_CODE)
    filepath = save_raw_data(data, COMPETITION_CODE)
    print(f"Extracción completa: {filepath}")


def task_transform():
    raw_data = load_latest_raw_file(COMPETITION_CODE)
    df = transform_matches(raw_data)

    os.makedirs("/opt/airflow/data/processed", exist_ok=True)
    output_path = "/opt/airflow/data/processed/wc_matches.csv"
    df.to_csv(output_path, index=False)
    print(f"Transformación completa: {output_path}")


def task_load():
    load_to_postgres("/opt/airflow/data/processed/wc_matches.csv")


default_args = {
    "owner": "gonzalo",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="football_world_cup_pipeline",
    default_args=default_args,
    description="ETL de partidos del Mundial 2026 desde football-data.org",
    schedule_interval=timedelta(hours=6),
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["football", "etl"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_matches",
        python_callable=task_extract,
    )

    transform_task = PythonOperator(
        task_id="transform_matches",
        python_callable=task_transform,
    )

    load_task = PythonOperator(
        task_id="load_matches",
        python_callable=task_load,
    )

    extract_task >> transform_task >> load_task