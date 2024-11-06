from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset(uri="/tmp/my_file.txt")
my_file_2 = Dataset(uri="/tmp/my_file_2.txt")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 4),
    'retries': 1,
}

with DAG('producer', default_args=default_args, schedule='@daily') as dag:
    
    @task(outlets=[my_file])
    def update_dataset():
        with open(my_file.uri, "a+") as f:
            f.write("producer update, ")
            
    @task(outlets=[my_file_2])
    def update_dataset_2():
        with open(my_file_2.uri, "a+") as f:
            f.write("producer update 2, ")
                
    update_dataset() >> update_dataset_2()