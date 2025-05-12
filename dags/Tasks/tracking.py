# tasks/track_data.py
import subprocess

def track_raw_data():
    # Track the raw data with DVC
    subprocess.run(['dvc', 'add', 'WeatherData/Lahore_Forecast.csv'])
    print("Raw data tracked with DVC")

def track_processed_data():
    # Track the processed data with DVC
    subprocess.run(['dvc', 'add', 'PreprocessedWeatherData/Processed_Lahore_Forecast.csv'])
    print("Processed data tracked with DVC")

def track_model():
    # Track the model with DVC
    subprocess.run(['dvc', 'add', 'models/linear_model.pkl'])
    print("Model tracked with DVC")
