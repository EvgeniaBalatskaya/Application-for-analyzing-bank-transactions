import unittest

from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import mask_sensitive_data, read_excel, read_json


class TestUtils(unittest.TestCase):
    @patch("src.utils.pd.read_excel")
    def test_read_excel_success(self, mock_read_excel):
        # Mock successful read_excel call
        mock_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        mock_read_excel.return_value = mock_df

        file_path = "test.xlsx"
        result = read_excel(file_path)

        # Check if the result matches the expected dataframe
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("src.utils.pd.read_excel")
    def test_read_excel_failure(self, mock_read_excel):
        # Mock read_excel to raise an exception
        mock_read_excel.side_effect = Exception("Read error")

        file_path = "test.xlsx"
        result = read_excel(file_path)

        # Check if the result is None
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_json_success(self, mock_file):
        file_path = "test.json"
        result = read_json(file_path)

        # Check if the result matches the expected dictionary
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", new_callable=mock_open)
    def test_read_json_failure(self, mock_file):
        # Mock open to raise an exception
        mock_file.side_effect = Exception("Read error")

        file_path = "test.json"
        result = read_json(file_path)

        # Check if the result is None
        self.assertIsNone(result)

    def test_mask_sensitive_data(self):
        data = "1234567890"
        masked_data = mask_sensitive_data(data)

        # Check if the masked data matches the expected masked string
        self.assertEqual(masked_data, "*" * len(data))

    def test_mask_sensitive_data_non_string(self):
        data = 1234567890
        masked_data = mask_sensitive_data(data)

        # Check if the non-string data is returned as is
        self.assertEqual(masked_data, data)


if __name__ == "__main__":
    unittest.main()
