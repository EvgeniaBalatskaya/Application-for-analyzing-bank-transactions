import json
import logging
from services import convert_xlsx_to_json, write_transactions_to_json, process_transaction, mask_data
from reports import generate_report_with_logging
from views import generate_report

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        # 1. Чтение данных о транзакциях из Excel
        transactions = convert_xlsx_to_json('transactions.xlsx')
        if not transactions:
            logger.error("Не удалось загрузить транзакции из файла.")
            return

        # 2. Обработка каждой транзакции (конвертация валюты и маскировка данных)
        processed_transactions = []
        for transaction in transactions:
            # Конвертируем валюту
            processed_transaction = process_transaction(transaction, 'USD', 'EUR')
            if processed_transaction:
                # Маскируем данные
                masked_transaction = mask_data(processed_transaction)
                processed_transactions.append(masked_transaction)

        # 3. Генерация отчета
        report = generate_report_with_logging(processed_transactions)
        logger.info("Отчет сгенерирован успешно.")

        # 4. Запись обработанных транзакций в JSON-файл
        write_transactions_to_json(processed_transactions, 'processed_transactions.json')

        # 5. Генерация отчета в формате JSON (для внешнего использования)
        external_report = generate_report(processed_transactions)
        with open('external_report.json', 'w', encoding='utf-8') as report_file:
            report_file.write(external_report)
        logger.info("Отчет внешнего формата сохранен в external_report.json.")

    except Exception as e:
        logger.error(f"Ошибка выполнения main: {e}")


if __name__ == "__main__":
    main()
