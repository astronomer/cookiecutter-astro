"""
This DAG serves as a hello world example. You can trigger this DAG manually to verify if your deployment can
run a task.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="hello_world",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    description=__doc__,
):
    hello = BashOperator(task_id="hello", bash_command="echo hello")
    world = PythonOperator(task_id="world", python_callable=lambda: print("world"))
    hello >> world
