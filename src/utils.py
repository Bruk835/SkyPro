import json
import os
from typing import Any


def load_transactions(file_path: Any) -> Any:
    """Загружает транзакции из JSON-файла."""
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        print(f"Файл пуст: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Данные не являются списком")
            return []

        return data

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    file_path = "../data/operations.json"

    transactions = load_transactions(file_path)
    print(f"Загружено {len(transactions)} транзакций")
