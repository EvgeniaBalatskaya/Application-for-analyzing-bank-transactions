import json
import logging
from datetime import datetime
from decimal import Decimal
import requests
import pandas as pd
from typing import List, Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для получения курса валют через внешний API (например, с использованием API Центробанка или других валютных сервисов)
def get_exchange_rate(from_currency: str, to_currency: str) -> Decimal:
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['rates'].get(to_currency)
        if rate:
            return Decimal(rate)
        else:
            logger.error(f"Курс для валюты {to_currency} не найден.")
            return Decimal(0)
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе курса валют: {e}")
        return Decimal(0)


# Функция для обработки транзакции и конвертации валюты
def process_transaction(transaction: Dict[str, Any], from_currency: str, to_currency: str) -> Dict[str, Any]:
    try:
        # Получаем курс валют
        exchange_rate = get_exchange_rate(from_currency, to_currency)
        if exchange_rate == 0:
            raise ValueError(f"Невозможно получить курс валют для {from_currency} -> {to_currency}")

        # Конвертируем сумму в нужную валюту
        amount_in_from_currency = Decimal(transaction['amount'])
        amount_in_to_currency = amount_in_from_currency * exchange_rate

        # Обновляем транзакцию
        transaction['amount_in_to_currency'] = str(amount_in_to_currency)
        transaction['exchange_rate'] = str(exchange_rate)
        transaction['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return transaction
    except Exception as e:
        logger.error(f"Ошибка обработки транзакции: {e}")
        return {}


# Функция для конвертации всех транзакций из XLSX в JSON
def convert_xlsx_to_json(xlsx_file_path: str) -> List[Dict[str, Any]]:
    try:
        # Чтение данных из Excel файла
        df = pd.read_excel(xlsx_file_path)

        # Преобразование данных в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при конвертации XLSX в JSON: {e}")
        return []


# Функция для записи транзакций в JSON-файл
def write_transactions_to_json(transactions: List[Dict[str, Any]], json_file_path: str) -> None:
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(transactions, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Транзакции успешно записаны в {json_file_path}")
    except Exception as e:
        logger.error(f"Ошибка при записи транзакций в JSON: {e}")


# Функция для маскировки данных в транзакциях (например, для защиты личных данных)
def mask_data(transaction: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Маскируем данные, например, заменяем номера карт на последние 4 цифры
        transaction['account_number'] = "**** **** **** " + transaction['account_number'][-4:]
        # Возвращаем маскированную транзакцию
        return transaction
    except Exception as e:
        logger.error(f"Ошибка при маскировке данных: {e}")
        return transaction
