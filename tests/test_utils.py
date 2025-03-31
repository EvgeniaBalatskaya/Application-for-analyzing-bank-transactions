import unittest

from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import mask_sensitive_data, read_excel, read_json


class TestUtils(unittest.TestCase):
    @patch("src.utils.pd.read_excel")
    def test_read_excel(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({"A": [1, 2, 3]})
        df = read_excel("dummy_path.xlsx")
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 1))

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_json(self, mock_file):
        data = read_json("dummy_path.json")
        self.assertIsNotNone(data)
        self.assertEqual(data, {"key": "value"})

    def test_mask_sensitive_data(self):
        sensitive_info = "1234-5678-9876-5432"
        masked = mask_sensitive_data(sensitive_info)
        self.assertEqual(masked, "*" * len(sensitive_info))


if __name__ == "__main__":
    unittest.main()
