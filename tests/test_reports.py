import pytest
from src.reports import get_exchange_rates, get_stock_prices, generate_report_with_logging
from unittest.mock import patch

def test_get_exchange_rates():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": {"USD": 1.0, "EUR": 0.9}
        }
        rates = get_exchange_rates()
        assert "USD" in rates
        assert "EUR" in rates

def test_get_stock_prices():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "AAPL": 150.0, "AMZN": 3200.0
        }
        prices = get_stock_prices()
        assert "AAPL" in prices
        assert "AMZN" in prices

def test_generate_report_with_logging():
    expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]
    with patch('src.reports.get_exchange_rates') as mock_get_exchange_rates:
        with patch('src.reports.get_stock_prices') as mock_get_stock_prices:
            mock_get_exchange_rates.return_value = {"USD": 1.0, "EUR": 0.9}
            mock_get_stock_prices.return_value = {"AAPL": 150.0, "AMZN": 3200.0}
            report = generate_report_with_logging(expenses)
            assert "expenses" in report
            assert "exchange_rates" in report
            assert "stock_prices" in report
