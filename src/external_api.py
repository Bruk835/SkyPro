import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


@lru_cache(maxsize=100)
def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты по отношению к рублю.

    Args:
        currency (str): Код валюты (USD, EUR)

    Returns:
        float: Курс конвертации в рубли

    Raises:
        Exception: Если API недоступен или ключ невалидный
    """
    if not API_KEY:
        raise Exception("API ключ не найден. Установите EXCHANGE_API_KEY в .env файле")

    url = f"{BASE_URL}"

    headers = {"apikey": API_KEY}

    params = {"from": currency.upper(), "to": "RUB", "amount": 1}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("success"):
            error_msg = data.get("error", {}).get("info", "Unknown error")
            raise Exception(f"API error: {error_msg}")

        return float(data["result"])

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при обращении к API: {e}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Ошибка парсинга ответа API: {e}")


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (dict): Словарь с данными транзакции,
                           содержащий ключи 'amount' и 'currency'

    Returns:
        float: Сумма в рублях

    Raises:
        ValueError: Если валюта не поддерживается или отсутствуют поля
        Exception: При ошибке конвертации через API
    """
    # Проверка наличия обязательных полей
    if "amount" not in transaction:
        raise ValueError("Транзакция не содержит поле 'amount'")

    if "currency" not in transaction:
        raise ValueError("Транзакция не содержит поле 'currency'")

    amount = transaction["amount"]
    currency = transaction["currency"].upper()

    # Проверка типа суммы
    if not isinstance(amount, (int, float)):
        raise ValueError(f"Сумма должна быть числом, получено: {type(amount).__name__}")

    # Если транзакция уже в рублях
    if currency == "RUB":
        return float(amount)

    # Конвертация для USD и EUR
    if currency in ("USD", "EUR"):
        try:
            exchange_rate = get_exchange_rate(currency)
            return float(amount * exchange_rate)
        except Exception as e:
            raise Exception(f"Ошибка конвертации {currency} в RUB: {e}")

    # Неподдерживаемая валюта
    raise ValueError(f"Неподдерживаемая валюта: {currency}. Поддерживаются: RUB, USD, EUR")
