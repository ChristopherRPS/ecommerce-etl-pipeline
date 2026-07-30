from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# Permite importar nuestros scripts desde src/
sys.path.append('/opt/airflow/src')

def run_extract():
    print("Extracción: los CSVs ya están en data/raw, no hace falta descargar nada extra")

def run_transform():
    exec(open('/opt/airflow/src/transform.py').read())

def run_load():
    exec(open('/opt/airflow/src/load.py').read())

default_args = {
    "owner": "data-engineer",
    "retries": 1,
}

with DAG(
    dag_id="ecommerce_etl_pipeline",
    default_args=default_args,
    description="Pipeline ETL de e-commerce (Olist)",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ecommerce", "etl"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=run_extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=run_transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=run_load,
    )

    extract_task >> transform_task >> load_task