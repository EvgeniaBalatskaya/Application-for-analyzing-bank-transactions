import json
import unittest

from datetime import datetime
from unittest.mock import MagicMock, patch

import requests

from src.views import generate_report, get_exchange_rates, get_stock_prices


class TestViews(unittest.TestCase):
    @patch("src.views.requests.get")
    def test_get_exchange_rates_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"rates": {"EUR": 0.85, "JPY": 110.0}}
        mock_get.return_value = mock_response

        result = get_exchange_rates()
        self.assertEqual(result, {"EUR": 0.85, "JPY": 110.0})

    @patch("src.views.requests.get")
    def test_get_exchange_rates_failure(self, mock_get):
        # Mock a failed API request
        mock_get.side_effect = requests.RequestException("API error")

        result = get_exchange_rates()
        self.assertEqual(result, {})

    @patch("src.views.requests.get")
    def test_get_stock_prices_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}
        mock_get.return_value = mock_response

        result = get_stock_prices()
        self.assertEqual(result, {"AAPL": 150.0, "GOOGL": 2800.0})

    @patch("src.views.requests.get")
    def test_get_stock_prices_failure(self, mock_get):
        # Mock a failed API request
        mock_get.side_effect = requests.RequestException("API error")

        result = get_stock_prices()
        self.assertEqual(result, {})

    @patch("src.views.get_exchange_rates")
    @patch("src.views.get_stock_prices")
    @patch("src.views.datetime")
    def test_generate_report(self, mock_datetime, mock_get_stock_prices, mock_get_exchange_rates):
        # Mock the return value of get_exchange_rates
        mock_get_exchange_rates.return_value = {"EUR": 0.85, "JPY": 110.0}

        # Mock the return value of get_stock_prices
        mock_get_stock_prices.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}

        # Mock the current date and time
        mock_datetime.now.return_value = datetime(2025, 3, 31, 16, 34, 34)

        # Sample expenses
        expenses = [{"category": "Food", "amount": 100.0}, {"category": "Transport", "amount": 50.0}]

        # Expected report
        expected_report = {
            "date": "2025-03-31T16:34:34",
            "expenses": expenses,
            "exchange_rates": {"EUR": 0.85, "JPY": 110.0},
            "stock_prices": {"AAPL": 150.0, "GOOGL": 2800.0},
        }

        # Generate the report
        report = generate_report(expenses)

        # Check if the report matches the expected report
        self.assertEqual(json.loads(report), expected_report)


if __name__ == "__main__":
    unittest.main()
