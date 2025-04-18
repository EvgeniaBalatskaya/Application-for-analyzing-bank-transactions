import json

from datetime import datetime

import requests


def get_exchange_rates():
    """Получить текущие курсы валют через API"""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()  # Поднимет исключение для плохого ответа
        data = response.json()
        return data["rates"]
    except requests.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return {}


def get_stock_prices():
    """Получить текущие цены на акции через API"""
    try:
        response = requests.get("https://api.stockprice-api.com/v1/prices")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Ошибка при получении цен на акции: {e}")
        return {}


def generate_report(expenses):
    """Генерация JSON-отчета с расходами и другими данными"""
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    report = {
        "date": datetime.now().isoformat(),
        "expenses": expenses,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(report, indent=4)


# Пример использования
if __name__ == "__main__":
    expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]
    print(generate_report(expenses))
