import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_cashback_categories(data: list, year: int, month: int) -> str:
    """
    Анализирует выгодные категории повышенного кешбэка.

    :param data: Список транзакций.
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :return: JSON с анализом.
    """
    analysis = {}
    for transaction in data:
        if transaction['Дата операции'].year == year and transaction['Дата операции'].month == month:
            category = transaction['Категория']
            cashback = transaction['Кешбэк']
            if category not in analysis:
                analysis[category] = 0
            analysis[category] += cashback

    logging.info("Analyzed cashback categories for %d-%02d", year, month)
    return json.dumps(analysis, ensure_ascii=False)