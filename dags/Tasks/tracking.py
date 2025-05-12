import subprocess
import mlflow
import mlflow.artifacts
mlflow.set_tracking_uri("http://localhost:5000")


def track_raw_data():
    # Track the raw data with DVC
    subprocess.run(['dvc', 'add', 'WeatherData/Lahore_Forecast.csv'])
    print("Raw data tracked with DVC")

    # Log the raw data as artifact in MLflow
    with mlflow.start_run(run_name="data_tracking"):
        mlflow.log_artifact('WeatherData/Lahore_Forecast.csv')
        print("Raw data tracked with MLflow")

def track_processed_data():
    # Track the processed data with DVC
    subprocess.run(['dvc', 'add', 'PreprocessedWeatherData/Processed_Lahore_Forecast.csv'])
    print("Processed data tracked with DVC")

    # Log the processed data as artifact in MLflow
    with mlflow.start_run(run_name="data_tracking"):
        mlflow.log_artifact('PreprocessedWeatherData/Processed_Lahore_Forecast.csv')
        print("Processed data tracked with MLflow")

def track_model():
    # Track the model with DVC
    subprocess.run(['dvc', 'add', 'models/linear_model.pkl'])
    print("Model tracked with DVC")

    # Log the model as artifact in MLflow
    with mlflow.start_run(run_name="model_tracking"):
        mlflow.log_artifact('models/linear_model.pkl')
        print("Model tracked with MLflow")
