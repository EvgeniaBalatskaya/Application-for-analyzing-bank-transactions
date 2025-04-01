import json
import logging

from typing import Any, Dict, Optional

import pandas as pd


logger = logging.getLogger(__name__)


def read_excel(file_path: str) -> Optional[pd.DataFrame]:
    """
    Чтение данных из Excel-файла
    """
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return None


def read_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Чтение данных из JSON-файла
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return None
    except Exception as e:
        print(f"Ошибка при чтении JSON-файла: {e}")
        return None


def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
    """
    Маскировка чувствительных данных (например, номеров карт)
    """
    if isinstance(data, str):
        return mask_char * len(data)
    return data
