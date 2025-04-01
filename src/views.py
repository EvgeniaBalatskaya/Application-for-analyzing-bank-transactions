import json
import logging

from datetime import datetime
from typing import Any, Dict, List

import requests


logger = logging.getLogger(__name__)


def get_exchange_rates() -> Dict[str, float]:
    logger.info("Получение курсов валют")
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()
        data = response.json()
        if isinstance(data["rates"], dict):
            logger.debug("Курсы валют успешно получены")
            return data["rates"]
        return {}
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return {}


def get_stock_prices() -> Dict[str, Any]:
    logger.info("Получение цен на акции")
    try:
        response = requests.get("https://api.stockprice-api.com/v1/prices")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            logger.debug("Цены на акции успешно получены")
            return data
        return {}
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении цен на акции: {e}")
        return {}


def generate_report(expenses: List[Dict[str, Any]]) -> str:
    logger.info("Генерация отчета")
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    report = {
        "date": datetime.now().isoformat(),
        "expenses": expenses,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    report_json = json.dumps(report, indent=4)
    logger.debug(f"Отчет сгенерирован: {report_json}")
    return report_json
