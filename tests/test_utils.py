import pytest
import pandas as pd
import json
from src.utils import read_transactions, load_user_settings
import os

# Создание временного Excel файла для тестов
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

# Создание временного JSON файла для тестов
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

def test_read_transactions(transactions_file):
    df = read_transactions(transactions_file)
    assert not df.empty
    assert len(df) == 3
    assert df['Дата операции'].iloc[0] == '2025-03-01'

def test_load_user_settings(user_settings_file):
    settings = load_user_settings(user_settings_file)
    assert 'user_currencies' in settings
    assert 'user_stocks' in settings
    assert settings['user_currencies'] == ["USD", "EUR"]
    assert settings['user_stocks'] == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
