import os

from src.services import analyze_expenses, calculate_cashback
from src.utils import mask_sensitive_data, read_excel, read_json
from src.views import generate_report


def main():
    # Чтение данных из файла
    file_path = "data/operations.xlsx"
    excel_data = read_excel(file_path)

    if excel_data is not None:
        # Преобразование данных в формат, который можем обработать
        expenses = excel_data.to_dict(orient="records")

        # Анализ расходов
        categorized_expenses = analyze_expenses(expenses)
        print(f"Categorized Expenses: {categorized_expenses}")

        # Расчет кешбэка
        cashback = calculate_cashback([], categorized_expenses)
        print(f"Cashback: {cashback}")

        # Генерация отчета
        report = generate_report(expenses)
        print(f"Generated Report: {report}")

    else:
        print("Не удалось загрузить данные из Excel-файла.")


if __name__ == "__main__":
    main()
