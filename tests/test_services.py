import pytest
import json
from datetime import datetime
from src.services import analyze_cashback_categories

def test_analyze_cashback_categories():
    data = [
        {'Дата операции': datetime(2025, 3, 1), 'Категория': 'Супермаркеты', 'Кешбэк': 10},
        {'Дата операции': datetime(2025, 3, 2), 'Категория': 'Супермаркеты', 'Кешбэк': 15},
        {'Дата операции': datetime(2025, 3, 3), 'Категория': 'Фастфуд', 'Кешбэк': 5}
    ]
    year = 2025
    month = 3
    response = analyze_cashback_categories(data, year, month)
    assert json.loads(response) == {'Супермаркеты': 25, 'Фастфуд': 5}