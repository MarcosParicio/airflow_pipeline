import os
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Imprimir variables de entorno para verificar
print("POSTGRES_USER:", os.getenv('POSTGRES_USER'))
print("POSTGRES_PASSWORD:", os.getenv('POSTGRES_PASSWORD'))
print("POSTGRES_DB:", os.getenv('POSTGRES_DB'))

# Función para extraer usuarios
def extract_users(**kwargs):
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='postgres',
        port='5432'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    # Empujar los datos extraídos a XCom
    kwargs['ti'].xcom_push(key='users', value=users)
    print("Usuarios extraídos:", users)

# Función para transformar usuarios
def transform_users(**kwargs):
    ti = kwargs['ti']
    users = ti.xcom_pull(key='users', task_ids='extract_users')
    print("Usuarios recibidos para transformar:", users)
    transformed_data = []
    for user in users:
        if len(user) >= 2:  # Asegúrate de que el usuario tenga al menos 2 elementos
            transformed_user = {
                'id': user[0],
                'full_name': f"{user[1]} {user[2]}",  # Combina first_name y last_name
                'email': user[3],
                'age': user[4]
            }
            transformed_data.append(transformed_user)
        else:
            print(f"Error: El usuario {user} no tiene suficientes elementos")
    # Empujar los datos transformados a XCom
    ti.xcom_push(key='transformed_users', value=transformed_data)
    print("Datos transformados:", transformed_data)

# Función para cargar usuarios
def load_users(**kwargs):
    ti = kwargs['ti']
    users = ti.xcom_pull(key='transformed_users', task_ids='transform_users')
    print("Usuarios recibidos para cargar:", users)
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='postgres',
        port='5432'
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO transformed_users (id, full_name, email, age)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (email) DO UPDATE SET
    id = EXCLUDED.id,
    full_name = EXCLUDED.full_name,
    age = EXCLUDED.age
    """
    for user in users:
        cursor.execute(insert_query, (user['id'], user['full_name'], user['email'], user['age']))
    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 3),
    'retries': 1,
}

with DAG('user_pipeline', default_args=default_args, schedule='@daily') as dag:

    extract_task = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
    )

    transform_task = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users,
    )

    load_task = PythonOperator(
        task_id='load_users',
        python_callable=load_users,
    )

    extract_task >> transform_task >> load_task