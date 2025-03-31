import unittest
from unittest.mock import patch, mock_open, MagicMock
import requests
import pandas as pd
from src.services import get_exchange_rate, process_transaction, convert_xlsx_to_json, write_transactions_to_json, \
    mask_data


class TestServicesFunctions(unittest.TestCase):

    @patch('services.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        # Мокируем успешный запрос к API
        mock_response = MagicMock()
        mock_response.json.return_value = {'rates': {'EUR': 0.85}}
        mock_get.return_value = mock_response

        result = get_exchange_rate('USD', 'EUR')

        self.assertEqual(result, 0.85)

    @patch('services.requests.get')
    def test_get_exchange_rate_failure(self, mock_get):
        # Мокируем ошибку при запросе
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = get_exchange_rate('USD', 'EUR')

        self.assertEqual(result, 0)

    def test_process_transaction_success(self):
        # Мокируем успешную обработку транзакции
        transaction = {'amount': 100, 'account_number': '1234-5678-9876-5432'}
        with patch('services.get_exchange_rate') as mock_rate:
            mock_rate.return_value = 0.85
            result = process_transaction(transaction, 'USD', 'EUR')

            self.assertEqual(result['amount_in_to_currency'], '85.00')
            self.assertEqual(result['exchange_rate'], '0.85')

    def test_process_transaction_failure(self):
        # Мокируем неудачную обработку транзакции
        transaction = {'amount': 100, 'account_number': '1234-5678-9876-5432'}
        with patch('services.get_exchange_rate') as mock_rate:
            mock_rate.return_value = 0
            result = process_transaction(transaction, 'USD', 'EUR')

            self.assertEqual(result, {})

    @patch('services.pd.read_excel')
    def test_convert_xlsx_to_json_success(self, mock_read_excel):
        # Мокируем успешное чтение Excel-файла
        mock_data = pd.DataFrame({"amount": [100, 200], "account_number": ['1234', '5678']})
        mock_read_excel.return_value = mock_data

        result = convert_xlsx_to_json('transactions.xlsx')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['amount'], 100)

    @patch('services.pd.read_excel')
    def test_convert_xlsx_to_json_failure(self, mock_read_excel):
        # Мокируем ошибку при чтении Excel-файла
        mock_read_excel.side_effect = Exception("Ошибка чтения файла")

        result = convert_xlsx_to_json('transactions.xlsx')

        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_write_transactions_to_json(self, mock_file):
        # Мокируем успешную запись в JSON-файл
        transactions = [{'amount': 100, 'account_number': '1234'}]
        write_transactions_to_json(transactions, 'transactions.json')

        mock_file.assert_called_once_with('transactions.json', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_write_transactions_to_json_failure(self, mock_file):
        # Мокируем ошибку при записи в JSON-файл
        mock_file.side_effect = Exception("Ошибка записи")
        transactions = [{'amount': 100, 'account_number': '1234'}]
        write_transactions_to_json(transactions, 'transactions.json')

        mock_file.assert_called_once_with('transactions.json', 'w', encoding='utf-8')

    def test_mask_data(self):
        # Проверка маскировки данных
        transaction = {'amount': 100, 'account_number': '1234-5678-9876-5432'}
        result = mask_data(transaction)

        self.assertEqual(result['account_number'], '**** **** **** 5432')


if __name__ == '__main__':
    unittest.main()
