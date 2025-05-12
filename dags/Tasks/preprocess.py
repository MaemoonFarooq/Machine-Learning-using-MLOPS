import pandas as pd
import os

def preprocess_data():
    # Load the raw data CSV file
    df = pd.read_csv('WeatherData/Lahore_Forecast.csv')
    
    # Example preprocessing: Drop rows with missing values
    df_cleaned = df.dropna()
    
    # Create the output directory if it doesn't exist
    output_dir = 'PreprocessedWeatherData'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the processed data as a new CSV file
    output_path = os.path.join(output_dir, 'Processed_Lahore_Forecast.csv')
    df_cleaned.to_csv(output_path, index=False)
    print("Data Preprocessed and Saved as processed_data.csv")
