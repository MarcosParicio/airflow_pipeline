from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset(uri="/tmp/my_file.txt")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 4),
    'retries': 1,
}

with DAG('consumer', default_args=default_args, schedule=[my_file]) as dag:
    
    @task
    def read_dataset():
        with open(my_file.uri, "r") as f:
            print(f.read())
            
    read_dataset()