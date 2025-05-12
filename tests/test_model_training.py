import unittest
from unittest.mock import patch, MagicMock, mock_open
import builtins
import pandas as pd

# Patch where it's imported
from dags.Tasks import model_training

class TestModelTraining(unittest.TestCase):

    @patch("dags.Tasks.model_training.pd.read_csv")
    @patch("dags.Tasks.model_training.pickle.dump")
    @patch("dags.Tasks.model_training.open", new_callable=mock_open)
    @patch("dags.Tasks.model_training.os.makedirs")
    def test_model_training_success(self, mock_makedirs, mock_open_file, mock_pickle_dump, mock_read_csv):
        # Sample dataframe
        mock_df = pd.DataFrame({
            'DateTime': ['2024-01-01 00:00:00'],
            'Humidity (%)': [40],
            'Wind Speed (m/s)': [5],
            'Weather Condition': ['clear sky'],
            'Temperature (°C)': [25]
        })

        mock_read_csv.return_value = mock_df

        # Run the function
        model_training.model_training()

        # Check that CSV was read
        mock_read_csv.assert_called_once()

        # Check that model file was attempted to be saved
        mock_open_file.assert_called_once_with('models/linear_model.pkl', 'wb')
        mock_pickle_dump.assert_called_once()

        # Check that models dir was created
        mock_makedirs.assert_called_once_with('models', exist_ok=True)

