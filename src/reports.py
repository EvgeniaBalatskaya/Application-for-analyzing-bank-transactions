import json
import logging

from datetime import datetime
from typing import Any, Dict, List

import requests


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


def generate_report(expenses: List[Dict[str, Any]]) -> str:
    """
    Генерация JSON-отчета с расходами и другими данными
    """
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    report = {
        "date": datetime.now().isoformat(),
        "expenses": expenses,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(report, indent=4)


def generate_report_with_logging(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    logging.info(f"Generated Report: {json.dumps(report, indent=4)}")
    return report
