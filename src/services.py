from typing import Any, Dict, List


def calculate_cashback(categories: List[str], spending: Dict[str, float]) -> Dict[str, float]:
    """
    Вычисление кэшбэка по категориям
    """
    cashback_rates = {
        "Food": 0.05,  # 5% кэшбэка
        "Transport": 0.03,  # 3% кэшбэка
        "Entertainment": 0.07,  # 7% кэшбэка
    }

    cashback: Dict[str, float] = {}
    for category, amount in spending.items():
        if category in cashback_rates:
            cashback[category] = amount * cashback_rates[category]

    return cashback


def analyze_expenses(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Анализ расходов, классификация по категориям
    """
    categorized_expenses: Dict[str, float] = {}
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        if category not in categorized_expenses:
            categorized_expenses[category] = 0.0
        categorized_expenses[category] += amount

    return categorized_expenses


# Пример использования
if __name__ == "__main__":
    spending = {"Food": 200.0, "Transport": 50.0, "Entertainment": 100.0}
    cashback = calculate_cashback([], spending)
    print("Cashback:", cashback)

    expenses = [
        {"category": "Food", "amount": 200.0},
        {"category": "Transport", "amount": 50.0},
        {"category": "Entertainment", "amount": 100.0},
        {"category": "Food", "amount": 50.0},
    ]
    print("Categorized Expenses:", analyze_expenses(expenses))
