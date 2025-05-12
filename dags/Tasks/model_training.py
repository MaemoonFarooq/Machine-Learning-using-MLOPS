import pandas as pd
import pickle
import os
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
mlflow.set_tracking_uri("http://localhost:5000")

def model_training():
    try:
        # Load dataset
        df = pd.read_csv('/home/maemoon/Documents/MLOPS_Project/PreprocessedWeatherData/Processed_Lahore_Forecast.csv')
        df = df.drop(columns=['DateTime'])

        # Encode categorical feature
        le = LabelEncoder()
        df['Weather Condition'] = le.fit_transform(df['Weather Condition'])

        # Split features and target
        X = df.drop(columns=['Temperature (°C)'])
        y = df['Temperature (°C)']

        # Model training
        model = LinearRegression()
        model.fit(X, y)

        # Predict for evaluation
        y_pred = model.predict(X)

        # Evaluation metrics
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        # Make models directory
        os.makedirs('models', exist_ok=True)

        # Save model locally
        with open('models/linear_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        print("✅ Model saved to models/linear_model.pkl")

        # --- MLflow Tracking ---
        with mlflow.start_run(run_name="linear_regression_weather"):
            mlflow.log_param("model_type", "LinearRegression")
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2_score", r2)

            # Log the model
            mlflow.sklearn.log_model(model, "linear_model")

            # Log the CSV as an artifact (optional)
            mlflow.log_artifact('/home/maemoon/Documents/MLOPS_Project/PreprocessedWeatherData/Processed_Lahore_Forecast.csv')

            print("📦 Model and metrics logged to MLflow")

    except ImportError:
        print("⚠️ Required libraries missing. Use 'pip install scikit-learn mlflow'")
