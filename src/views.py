import json
import pandas as pd
from datetime import datetime
import requests
import logging
from src.utils import read_transactions

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_greeting(current_time: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    :param current_time: Текущее время.
    :return: Приветствие.
    """
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_info(transactions: pd.DataFrame) -> list:
    """
    Возвращает информацию по каждой карте: последние 4 цифры, общая сумма расходов и кешбэк.

    :param transactions: DataFrame с транзакциями.
    :return: Список словарей с информацией по картам.
    """
    cards = {}
    for _, row in transactions.iterrows():
        card = row['Номер карты']
        if card not in cards:
            cards[card] = {'total_spent': 0, 'cashback': 0}
        cards[card]['total_spent'] += row['Сумма платежа']
        cards[card]['cashback'] += row['Кешбэк']

    return [{'last_digits': card[-4:], 'total_spent': info['total_spent'], 'cashback': info['cashback']} for card, info
            in cards.items()]


def get_top_transactions(transactions: pd.DataFrame, top_n: int = 5) -> list:
    """
    Возвращает топ N транзакций по сумме платежа.

    :param transactions: DataFrame с транзакциями.
    :param top_n: Количество транзакций для возврата.
    :return: Список словарей с информацией о топ транзакциях.
    """
    return transactions.nlargest(top_n, 'Сумма платежа')[
        ['Дата операции', 'Сумма платежа', 'Категория', 'Описание']].to_dict(orient='records')


def get_currency_rates(currencies: list) -> list:
    """
    Возвращает курс валют для заданных валют.

    :param currencies: Список валют.
    :return: Список словарей с курсами валют.
    """
    rates = []
    for currency in currencies:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{currency}')
        rate = response.json()['rates']['RUB']
        rates.append({'currency': currency, 'rate': rate})
    return rates


def get_stock_prices(stocks: list) -> list:
    """
    Возвращает стоимость акций для заданных компаний.

    :param stocks: Список компаний.
    :return: Список словарей с ценами на акции.
    """
    prices = []
    for stock in stocks:
        response = requests.get(f'https://api.stock-api.com/{stock}')
        price = response.json()['price']
        prices.append({'stock': stock, 'price': price})
    return prices


def main_page(date_str: str, transactions: pd.DataFrame, user_settings: dict) -> dict:
    """
    Основная функция для генерации JSON-ответа для страницы "Главная".

    :param date_str: Строка с датой и временем в формате YYYY-MM-DD HH:MM:SS.
    :param transactions: DataFrame с транзакциями.
    :param user_settings: Словарь с пользовательскими настройками.
    :return: JSON-ответ.
    """
    current_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(current_time)

    transactions = transactions[(transactions['Дата операции'] >= current_time.replace(day=1)) & (
                transactions['Дата операции'] <= current_time)]

    card_info = get_card_info(transactions)
    top_transactions = get_top_transactions(transactions)

    currency_rates = get_currency_rates(user_settings['user_currencies'])
    stock_prices = get_stock_prices(user_settings['user_stocks'])

    response = {
        'greeting': greeting,
        'cards': card_info,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }

    logging.info("Generated main page response")
    return response
