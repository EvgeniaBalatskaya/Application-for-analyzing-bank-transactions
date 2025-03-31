import pytest
import pandas as pd
from datetime import datetime
from src.reports import spending_by_category

@pytest.fixture
def transactions():
    data = {
        'Дата операции': [datetime(2025, 1, 1), datetime(2025, 2, 1), datetime(2025, 3, 1)],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты'],
        'Сумма платежа': [100, 200, 300]
    }
    return pd.DataFrame(data)

def test_spending_by_category(transactions):
    category = 'Супермаркеты'
    date = '2025-03-31'
    response = spending_by_category(transactions, category, date)
    assert response['Сумма платежа'].sum() == 600