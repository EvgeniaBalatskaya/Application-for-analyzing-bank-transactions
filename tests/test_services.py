import pytest
from src.services import calculate_cashback, analyze_expenses

def test_calculate_cashback():
    spending = {"Food": 200, "Transport": 50, "Entertainment": 100}
    cashback = calculate_cashback([], spending)
    assert cashback["Food"] == 200 * 0.05
    assert cashback["Transport"] == 50 * 0.03
    assert cashback["Entertainment"] == 100 * 0.07

def test_analyze_expenses():
    expenses = [
        {"category": "Food", "amount": 200},
        {"category": "Transport", "amount": 50},
        {"category": "Entertainment", "amount": 100},
        {"category": "Food", "amount": 50},
    ]
    categorized_expenses = analyze_expenses(expenses)
    assert categorized_expenses["Food"] == 250
    assert categorized_expenses["Transport"] == 50
    assert categorized_expenses["Entertainment"] == 100
