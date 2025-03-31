import pytest
import json
from src.main import run_main
from unittest.mock import patch
import pandas as pd
import os

@pytest.fixture
def transactions_file(tmp_path):
    data = {
        'Дата операции': ['2025-03-01', '2025-03-02', '2025-03-03'],
        'Дата платежа': ['2025-03-01', '2025-03-02', '2025-03-03'],
        'Номер карты': ['1234', '5678', '1234'],
        'Статус': ['OK', 'OK', 'OK'],
        'Сумма операции': [100, 200, 300],
        'Валюта операции': ['USD', 'USD', 'USD'],
        'Сумма платежа': [100, 200, 300],
        'Валюта платежа': ['RUB', 'RUB', 'RUB'],
        'Кешбэк': [1, 2, 3],
        'Категория': ['Супермаркеты', 'Фастфуд', 'Супермаркеты'],
        'MCC': [5411, 5814, 5411],
        'Описание': ['Покупка в магазине', 'Покупка в фастфуде', 'Покупка в магазине'],
        'Бонусы (включая кешбэк)': [1, 2, 3],
        'Округление на «Инвесткопилку»': [0, 0, 0],
        'Сумма операции с округлением': [100, 200, 300]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "operations.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

@pytest.fixture
def user_settings_file(tmp_path):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    file_path = tmp_path / "user_settings.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path

@patch('builtins.print')
def test_run_main(mock_print, transactions_file, user_settings_file):
    with patch('src.main.read_transactions') as mock_read_transactions:
        with patch('src.main.load_user_settings') as mock_load_user_settings:
            mock_read_transactions.return_value = pd.read_excel(transactions_file)
            mock_load_user_settings.return_value = json.load(open(user_settings_file))

            run_main()

            assert mock_print.called
            output = mock_print.call_args[0][0]
            response = json.loads(output)
            assert 'greeting' in response
            assert 'cards' in response
            assert 'top_transactions' in response
            assert 'currency_rates' in response
            assert 'stock_prices' in response
