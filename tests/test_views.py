import pytest
import pandas as pd
import json
from datetime import datetime
from src.views import main_page, read_transactions

@pytest.fixture
def transactions():
    data = {
        'Дата операции': [datetime(2025, 3, 1), datetime(2025, 3, 2), datetime(2025, 3, 3)],
        'Номер карты': ['1234', '5678', '1234'],
        'Сумма платежа': [100, 200, 300],
        'Кешбэк': [1, 2, 3],
        'Категория': ['Супермаркеты', 'Фастфуд', 'Супермаркеты'],
        'Описание': ['Покупка 1', 'Покупка 2', 'Покупка 3']
    }
    return pd.DataFrame(data)

@pytest.fixture
def user_settings():
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }

def test_main_page(transactions, user_settings):
    date_str = "2025-03-31 12:37:12"
    response = main_page(date_str, transactions, user_settings)
    assert 'greeting' in response
    assert 'cards' in response
    assert 'top_transactions' in response
    assert 'currency_rates' in response
    assert 'stock_prices' in response