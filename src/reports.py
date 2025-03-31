import json
import logging
from datetime import datetime
from functools import wraps
import requests

# Настроим логирование
logging.basicConfig(level=logging.INFO, filename="reports.log", filemode="a", format="%(asctime)s - %(message)s")

def log_report(func):
    """
    Декоратор для логирования отчетов
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        report = func(*args, **kwargs)
        logging.info(f"Generated Report: {json.dumps(report, indent=4)}")
        return report
    return wrapper

def get_exchange_rates():
    """
    Получить текущие курсы валют через API
    """
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()  # Поднимет исключение для плохого ответа
        data = response.json()
        return data["rates"]
    except requests.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return {}

def get_stock_prices():
    """
    Получить текущие цены на акции через API
    """
    try:
        response = requests.get("https://api.stockprice-api.com/v1/prices")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Ошибка при получении цен на акции: {e}")
        return {}

@log_report
def generate_report_with_logging(expenses):
    """
    Генерация отчета с логированием
    """
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    report = {
        "date": datetime.now().isoformat(),
        "expenses": expenses,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }
    return report

# Пример использования
if __name__ == "__main__":
    expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]
    print(generate_report_with_logging(expenses))
