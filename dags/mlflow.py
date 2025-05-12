# dags/data_pipeline_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Import the functions from the separate task files
from Tasks.datacollection import data_collection
from Tasks.preprocess import preprocess_data
from Tasks.tracking import track_raw_data, track_processed_data, track_model
from Tasks.model_training import model_training as train_model  # Avoid name conflict

# Define the DAG
dag = DAG(
    'data_pipeline_dag',
    description='A simple data collection and preprocessing DAG',
    schedule_interval='@once',
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the tasks
collect_data_task = PythonOperator(
    task_id='collect_data',
    python_callable=data_collection,
    dag=dag,
)

track_raw_task = PythonOperator(
    task_id='track_raw_data',
    python_callable=track_raw_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

track_processed_task = PythonOperator(
    task_id='track_processed_data',
    python_callable=track_processed_data,
    dag=dag,
)

model_training_task = PythonOperator(  # Renamed to avoid name conflict
    task_id='model_training',
    python_callable=train_model,
    dag=dag,
)

track_model_task = PythonOperator(
    task_id='track_model',
    python_callable=track_model,
    dag=dag,
)


# Set task dependencies
collect_data_task >> track_raw_task >> preprocess_data_task >> track_processed_task >> model_training_task >> track_model_task