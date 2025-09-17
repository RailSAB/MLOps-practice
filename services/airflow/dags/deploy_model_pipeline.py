from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from pendulum import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DEPLOY_DIR = BASE_DIR / "code" / "deployment"

with DAG(
    dag_id="deploy_model_pipeline",
    schedule=None,
    start_date=datetime(2025, 9, 15, tz="Europe/Moscow"),
    catchup=False,
) as dag:

    compose_build = BashOperator(
        task_id="docker_compose_build",
        bash_command=f"cd {DEPLOY_DIR} && docker compose build"
    )

    compose_up = BashOperator(
        task_id="docker_compose_up",
        bash_command=f"cd {DEPLOY_DIR} && docker compose up -d --remove-orphans"
    )

    compose_build >> compose_up