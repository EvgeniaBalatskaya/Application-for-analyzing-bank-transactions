import unittest
from unittest.mock import patch, MagicMock
import json
from src.reports import get_exchange_rates, get_stock_prices, generate_report_with_logging


class TestReportsFunctions(unittest.TestCase):

    @patch('reports.requests.get')
    def test_get_exchange_rates_success(self, mock_get):
        # Мокируем успешный запрос для курсов валют
        mock_response = MagicMock()
        mock_response.json.return_value = {'rates': {'EUR': 0.85}}
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        self.assertEqual(result, {'EUR': 0.85})

    @patch('reports.requests.get')
    def test_get_exchange_rates_failure(self, mock_get):
        # Мокируем ошибку при запросе курсов валют
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = get_exchange_rates()

        self.assertEqual(result, {})

    @patch('reports.requests.get')
    def test_get_stock_prices_success(self, mock_get):
        # Мокируем успешный запрос для цен на акции
        mock_response = MagicMock()
        mock_response.json.return_value = {'AAPL': 150.0}
        mock_get.return_value = mock_response

        result = get_stock_prices()

        self.assertEqual(result, {'AAPL': 150.0})

    @patch('reports.requests.get')
    def test_get_stock_prices_failure(self, mock_get):
        # Мокируем ошибку при запросе цен на акции
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = get_stock_prices()

        self.assertEqual(result, {})

    @patch('reports.get_exchange_rates')
    @patch('reports.get_stock_prices')
    @patch('reports.logging.info')
    def test_generate_report_with_logging(self, mock_info, mock_get_stock_prices, mock_get_exchange_rates):
        # Мокируем функции для получения курсов валют и цен на акции
        mock_get_exchange_rates.return_value = {'EUR': 0.85}
        mock_get_stock_prices.return_value = {'AAPL': 150.0}

        expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]

        # Генерация отчета
        result = generate_report_with_logging(expenses)

        # Проверяем, что логирование вызвалось
        mock_info.assert_called_once()

        # Проверяем правильность отчета
        expected_report = {
            "date": result['date'],  # Дата будет динамической
            "expenses": expenses,
            "exchange_rates": {'EUR': 0.85},
            "stock_prices": {'AAPL': 150.0}
        }

        # Проверка на соответствие структуры отчета
        self.assertTrue(json.dumps(result, indent=4), json.dumps(expected_report, indent=4))


if __name__ == '__main__':
    unittest.main()
