from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from streaming_to_kafka import data_to_kafka
default_args = {
    'owner': 'Quyendinh',
    'start_date': datetime(2025, 1, 1),
    'depend_on_past': False
}


with DAG('push_data_to_broker',
         default_args=default_args,
         schedule='@hourly',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api_to_broker',
        python_callable=data_to_kafka
    )
