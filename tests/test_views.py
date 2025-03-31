import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
from src.views import get_exchange_rates, get_stock_prices, generate_report


class TestFinancialFunctions(unittest.TestCase):

    @patch('views.requests.get')
    def test_get_exchange_rates_success(self, mock_get):
        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {
                "EUR": 0.85,
                "GBP": 0.75
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        self.assertEqual(result, {"EUR": 0.85, "GBP": 0.75})
        mock_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")

    @patch('views.requests.get')
    def test_get_exchange_rates_failure(self, mock_get):
        # Мокируем ошибку при запросе
        mock_get.side_effect = requests.RequestException("Ошибка сети")

        result = get_exchange_rates()

        self.assertEqual(result, {})

    @patch('views.requests.get')
    def test_get_stock_prices_success(self, mock_get):
        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.json.return_value = [{"symbol": "AAPL", "price": 150}]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_stock_prices()

        self.assertEqual(result, [{"symbol": "AAPL", "price": 150}])
        mock_get.assert_called_once_with("https://api.stockprice-api.com/v1/prices")

    @patch('views.requests.get')
    def test_get_stock_prices_failure(self, mock_get):
        # Мокируем ошибку при запросе
        mock_get.side_effect = requests.RequestException("Ошибка сети")

        result = get_stock_prices()

        self.assertEqual(result, {})

    @patch('views.get_exchange_rates')
    @patch('views.get_stock_prices')
    def test_generate_report(self, mock_get_stock_prices, mock_get_exchange_rates):
        # Мокируем функции для получения данных
        mock_get_exchange_rates.return_value = {"EUR": 0.85, "GBP": 0.75}
        mock_get_stock_prices.return_value = [{"symbol": "AAPL", "price": 150}]

        expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]
        expected_report = {
            "date": datetime.now().isoformat(),
            "expenses": expenses,
            "exchange_rates": {"EUR": 0.85, "GBP": 0.75},
            "stock_prices": [{"symbol": "AAPL", "price": 150}]
        }

        result = generate_report(expenses)

        # Проверяем, что результат является строкой JSON и содержит ожидаемую информацию
        self.assertIsInstance(result, str)
        self.assertEqual(json.loads(result)['expenses'], expenses)
        self.assertEqual(json.loads(result)['exchange_rates'], {"EUR": 0.85, "GBP": 0.75})
        self.assertEqual(json.loads(result)['stock_prices'], [{"symbol": "AAPL", "price": 150}])


if __name__ == '__main__':
    unittest.main()
