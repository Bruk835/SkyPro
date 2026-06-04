import json
import logging
import os
from typing import Any

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: Any) -> Any:
    """Загружает транзакции из JSON-файла."""

    logger.info(f"Начало загрузки транзакций из файла: {file_path}")
    logger.debug(f"Тип file_path: {type(file_path)}")

    if not os.path.exists(file_path):
        error_msg = f"Файл не найден: {file_path}"
        logger.error(error_msg)
        print(error_msg)
        return []

    if os.path.getsize(file_path) == 0:
        error_msg = f"Файл пуст: {file_path}"
        logger.warning(error_msg)
        print(error_msg)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"JSON успешно загружен, тип данных: {type(data)}")

        if not isinstance(data, list):
            error_msg = "Данные не являются списком"
            logger.error(f"{error_msg}. Получен тип: {type(data)}")
            print(error_msg)
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")

        return data

    except FileNotFoundError as e:
        error_msg = f"Файл не найден при попытке открытия: {e}"
        logger.error(error_msg, exc_info=True)
        print(f"Ошибка: {e}")
        return []
    except (json.JSONDecodeError, IOError) as e:
        error_msg = f"Ошибка декодирования JSON в файле {file_path}: {e}"
        logger.error(error_msg, exc_info=True)
        print(f"Ошибка при чтении файла: некорректный JSON формат")
        return []


if __name__ == "__main__":
    file_path = "../data/operations.json"

    transactions = load_transactions(file_path)
    print(f"Загружено {len(transactions)} транзакций")
