import unittest
from unittest.mock import patch

from src.views import generate_report, get_exchange_rates, get_stock_prices


class TestViews(unittest.TestCase):
    @patch("src.views.get_exchange_rates")
    @patch("src.views.get_stock_prices")
    def test_generate_report(self, mock_get_stock_prices, mock_get_exchange_rates):
        mock_get_exchange_rates.return_value = {"USD": 1.0, "EUR": 0.9}
        mock_get_stock_prices.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}

        expenses = [{"category": "Food", "amount": 100.0}, {"category": "Transport", "amount": 50.0}]
        report = generate_report(expenses)

        self.assertIn("date", report)
        self.assertIn("expenses", report)
        self.assertIn("exchange_rates", report)
        self.assertIn("stock_prices", report)

    @patch("requests.get")
    def test_get_exchange_rates(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.9}}
        mock_get.return_value.raise_for_status = lambda: None

        rates = get_exchange_rates()
        self.assertEqual(rates, {"USD": 1.0, "EUR": 0.9})

    @patch("requests.get")
    def test_get_stock_prices(self, mock_get):
        mock_get.return_value.json.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}
        mock_get.return_value.raise_for_status = lambda: None

        prices = get_stock_prices()
        self.assertEqual(prices, {"AAPL": 150.0, "GOOGL": 2800.0})


if __name__ == "__main__":
    unittest.main()
