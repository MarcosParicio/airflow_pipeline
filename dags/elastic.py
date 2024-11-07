import sys
import os
# Permite que el script acceda a los módulos del directorio raíz subiendo un nivel más arriba de donde nos encontramos:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator

from plugins.hooks.elastic.elastic_hook import ElasticHook

from datetime import datetime
 
def _print_es_info():
    hook = ElasticHook()
    print(hook.info())

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 6),
    'retries': 1,
}

with DAG('elastic_dag', default_args=default_args, schedule='@daily') as dag:
 
    print_es_info = PythonOperator(
        task_id='print_es_info',
        python_callable=_print_es_info
    )