from airflow import DAG
from airflow.operators.bash import BashOperator

from task_groups.task_group_downloads import download_tasks
from task_groups.task_group_transforms import transform_tasks
    
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 5),
    'retries': 1,
}

with DAG('group_dag_task_groups', default_args=default_args, schedule='@daily') as dag:
    
    downloads = download_tasks()
    
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
    
    transforms = transform_tasks()
    
    downloads >> check_files >> transforms