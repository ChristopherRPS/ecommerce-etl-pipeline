from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
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

DBT_DIR = "/opt/airflow/olist_dbt"
DBT_PROFILES = "/opt/airflow/olist_dbt"

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
    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run --profiles-dir {DBT_PROFILES} --profile olist_dbt --target dev --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )
    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )
    drop_dbt_views = BashOperator(
        task_id="drop_dbt_views",
        bash_command=(
            "PGPASSWORD=etl_pass psql -h postgres -U etl_user -d ecommerce_dw "
            "-c 'DROP SCHEMA IF EXISTS dbt_olist CASCADE;'"
        ),
    )

    extract_task >> transform_task >> drop_dbt_views >> load_task >> dbt_run_task >> dbt_test_task