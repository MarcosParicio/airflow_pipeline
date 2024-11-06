from airflow import DAG, Dataset
from airflow.decorators import task
import os

from datetime import datetime

my_file = Dataset(uri="/tmp/my_file.txt")
my_file_2 = Dataset(uri="/tmp/my_file_2.txt")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 4),
    'retries': 1,
}

with DAG('consumer', default_args=default_args, schedule=[my_file, my_file_2]) as dag:
    
    @task
    def read_datasets():
        if os.path.exists(my_file.uri) and os.path.exists(my_file_2.uri):
            with open(my_file.uri, "r") as f1, open(my_file_2.uri, "r") as f2:
                print(f1.read())
                print(f2.read())
        else:
            raise FileNotFoundError("Uno o ambos archivos no existen.")
            
    read_datasets()