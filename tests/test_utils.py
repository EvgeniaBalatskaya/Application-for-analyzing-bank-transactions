import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import pandas as pd
from src.utils import read_excel, read_json, mask_sensitive_data


class TestUtilsFunctions(unittest.TestCase):

    @patch('utils.pd.read_excel')
    def test_read_excel_success(self, mock_read_excel):
        # Мокируем успешное чтение Excel-файла
        mock_data = pd.DataFrame({"Column1": [1, 2, 3], "Column2": [4, 5, 6]})
        mock_read_excel.return_value = mock_data

        result = read_excel("data/operations.xlsx")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (3, 2))  # Проверяем размер данных

    @patch('utils.pd.read_excel')
    def test_read_excel_failure(self, mock_read_excel):
        # Мокируем ошибку при чтении Excel-файла
        mock_read_excel.side_effect = Exception("Ошибка чтения файла")

        result = read_excel("data/operations.xlsx")

        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_json_success(self, mock_file):
        # Мокируем успешное чтение JSON-файла
        result = read_json("data/transactions.json")

        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once_with("data/transactions.json", "r")

    @patch("builtins.open", new_callable=mock_open)
    def test_read_json_failure(self, mock_file):
        # Мокируем ошибку при чтении JSON-файла
        mock_file.side_effect = Exception("Ошибка чтения файла")

        result = read_json("data/transactions.json")

        self.assertIsNone(result)

    def test_mask_sensitive_data(self):
        # Проверяем маскировку строки
        sensitive_data = "1234-5678-9876-5432"
        result = mask_sensitive_data(sensitive_data)

        self.assertEqual(result, "****************")

        # Проверяем, что данные не строкового типа не маскируются
        non_sensitive_data = 12345
        result_non_sensitive = mask_sensitive_data(non_sensitive_data)

        self.assertEqual(result_non_sensitive, 12345)


if __name__ == '__main__':
    unittest.main()
