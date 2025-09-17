from pendulum import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_SCRIPT = BASE_DIR / "code" / "models" / "logistic_exp1.py"

with DAG(
    dag_id="model_training_dag_simple",
    schedule=None,
    start_date=datetime(2025, 9, 14, hour=14, tz="Europe/Moscow"),
    catchup=False,
) as dag:

    train_model_task = BashOperator(
        task_id="train_model",
        bash_command=f"python3 {MODEL_SCRIPT}",
    )

    train_model_task