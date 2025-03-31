import os
import sys
import json

# Добавление корневого каталога проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import analyze_expenses, calculate_cashback
from src.utils import read_excel
from src.views import generate_report

def main() -> None:
    # Чтение данных из файла
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../data/operations.xlsx")
    excel_data = read_excel(file_path)

    if excel_data is not None:
        # Преобразование данных в формат, который можем обработать
        expenses = []
        for record in excel_data.to_dict(orient="records"):
            if "Категория" in record and "Сумма операции" in record:
                expenses.append({
                    "category": record["Категория"],
                    "amount": record["Сумма операции"],
                })
            else:
                print(f"Запись пропущена из-за отсутствия ключей: {record}")

        if not expenses:
            print("Нет действительных записей для обработки.")
            return

        # Анализ расходов
        categorized_expenses = analyze_expenses(expenses)
        print(f"Categorized Expenses: {json.dumps(categorized_expenses, ensure_ascii=False, indent=4)}")

        # Расчет кэшбэка
        cashback = calculate_cashback([], categorized_expenses)
        print(f"Cashback: {json.dumps(cashback, ensure_ascii=False, indent=4)}")

        # Генерация отчета
        report = generate_report(expenses)
        report_json = json.loads(report)
        print(f"Generated Report: {json.dumps(report_json, ensure_ascii=False, indent=4)}")

    else:
        print("Не удалось загрузить данные из Excel-файла.")

if __name__ == "__main__":
    main()
