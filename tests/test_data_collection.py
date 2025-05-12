import unittest
from unittest.mock import patch
from dags.Tasks.datacollection import data_collection

class TestDataCollection(unittest.TestCase):

    @patch('dags.Tasks.datacollection.requests.get')
    def test_data_collection_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'list': [{
                'dt_txt': '2025-05-12 12:00:00',
                'main': {'temp': 30, 'humidity': 50},
                'wind': {'speed': 5},
                'weather': [{'description': 'clear sky'}]
            }]
        }

        with patch('dags.Tasks.datacollection.pd.DataFrame.to_csv') as mock_to_csv:
            data_collection()
            mock_to_csv.assert_called_once()
