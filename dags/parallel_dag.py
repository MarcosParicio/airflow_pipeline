from airflow import DAG
from airflow.operators.bash import BashOperator
    
from datetime import datetime
    
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 5),
    'retries': 1,
}

with DAG('parallel_dag', default_args=default_args, schedule='@daily') as dag:
    
    extract_a = BashOperator(
        task_id='extract_a',
        bash_command='sleep 10'
    )
    
    extract_b = BashOperator(
        task_id='extract_b',
        bash_command='sleep 10'
    )
    
    load_a = BashOperator(
        task_id='load_a',
        bash_command='sleep 10'
    )
    
    load_b = BashOperator(
        task_id='load_b',
        bash_command='sleep 10'
    )
    
    transform = BashOperator(
        task_id='transform',
        bash_command='sleep 10'
    )
    
    extract_a >> load_a
    extract_b >> load_b
    [load_a, load_b] >> transform