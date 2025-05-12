import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from dags.Tasks import preprocess

class TestPreprocess(unittest.TestCase):

    @patch("dags.Tasks.preprocess.pd.read_csv")
    @patch("dags.Tasks.preprocess.os.makedirs")
    @patch("dags.Tasks.preprocess.pd.DataFrame.to_csv")
    def test_preprocess_data(self, mock_to_csv, mock_makedirs, mock_read_csv):
        # Create mock DataFrame
        mock_df = pd.DataFrame({
            'DateTime': ['2024-01-01 00:00:00', None],
            'Temperature (°C)': [25, None],
            'Humidity (%)': [40, 50],
            'Wind Speed (m/s)': [5, 4],
            'Weather Condition': ['clear sky', 'cloudy']
        })

        # Return mock dataframe
        mock_read_csv.return_value = mock_df

        # Call function
        preprocess.preprocess_data()

        # Check if CSV was read
        mock_read_csv.assert_called_once_with('WeatherData/Lahore_Forecast.csv')

        # Check if dropna was applied and saved
        mock_to_csv.assert_called_once()
        mock_makedirs.assert_called_once_with('PreprocessedWeatherData', exist_ok=True)
