import pandas as pd
import pickle
import os

def model_training():
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import LabelEncoder

        # Load CSV
        df = pd.read_csv('/home/maemoon/Documents/MLOPS_Project/PreprocessedWeatherData/Processed_Lahore_Forecast.csv')

        # Drop DateTime
        df = df.drop(columns=['DateTime'])

        # Encode weather condition to numbers
        le = LabelEncoder()
        df['Weather Condition'] = le.fit_transform(df['Weather Condition'])

        # Features and target
        X = df.drop(columns=['Temperature (°C)'])
        y = df['Temperature (°C)']

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)

        # Save model to models/linear_model.pkl
        with open('models/linear_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        print("✅ Model saved to models/linear_model.pkl")
    except ImportError:
        print("⚠️ scikit-learn is not installed. Please install it using 'pip install scikit-learn'")
        print("⚠️ Model training skipped due to missing dependencies")
