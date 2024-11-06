from airflow import DAG
from airflow.operators.bash import BashOperator
    
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 5),
    'retries': 1,
}

with DAG('group_dag', default_args=default_args, schedule='@daily') as dag:
    
    download_a = BashOperator(
        task_id='download_a',
        bash_command='sleep 10'
    )
    
    download_b = BashOperator(
        task_id='download_b',
        bash_command='sleep 10'
    )
    
    download_c = BashOperator(
        task_id='download_c',
        bash_command='sleep 10'
    )
    
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
    
    transform_a = BashOperator(
        task_id='transform_a',
        bash_command='sleep 10'
    )
    
    transform_b = BashOperator(
        task_id='transform_b',
        bash_command='sleep 10'
    )
    
    transform_c = BashOperator(
        task_id='transform_c',
        bash_command='sleep 10'
    )
    
    [download_a, download_b, download_c] >> check_files >> [transform_a, transform_b, transform_c]