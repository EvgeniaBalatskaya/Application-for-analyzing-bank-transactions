import json
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца от переданной даты.

    :param transactions: DataFrame с транзакциями.
    :param category: Название категории.
    :param date: Дата отсчета трехмесячного периода.
    :return: DataFrame с тратами по заданной категории.
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    three_months_ago = date - timedelta(days=90)
    filtered_transactions = transactions[
        (transactions['Категория'] == category) & (transactions['Дата операции'] >= three_months_ago) & (
                    transactions['Дата операции'] <= date)]

    logging.info("Generated spending report for category '%s' from %s to %s", category,
                 three_months_ago.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"))
    return filtered_transactions.groupby('Категория')['Сумма платежа'].sum().reset_index()
