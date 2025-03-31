import json
import logging

from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict

import requests


# Настроим логирование
logging.basicConfig(level=logging.INFO, filename="reports.log", filemode="a", format="%(asctime)s - %(message)s")


def log_report(func: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
    """
    Декоратор для логирования отчетов
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        report = func(*args, **kwargs)
        logging.info(f"Generated Report: {json.dumps(report, indent=4)}")
        return report

    return wrapper


def get_exchange_rates() -> Dict[str, float]:
    """
    Получить текущие курсы валют через API
    """
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()  # Поднимет исключение для плохого ответа
        data = response.json()
        if isinstance(data["rates"], dict):
            return data["rates"]
        return {}
    except requests.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return {}


def get_stock_prices() -> Dict[str, Any]:
    """
    Получить текущие цены на акции через API
    """
    try:
        response = requests.get("https://api.stockprice-api.com/v1/prices")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data
        return {}
    except requests.RequestException as e:
        print(f"Ошибка при получении цен на акции: {e}")
        return {}


@log_report
def generate_report_with_logging(expenses: list) -> Dict[str, Any]:
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
    expenses = [{"category": "Food", "amount": 100.0}, {"category": "Transport", "amount": 50.0}]
    print(generate_report_with_logging(expenses))
