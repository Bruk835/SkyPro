import json
import os

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")


def amount_in_rub(transaction: dict) -> float:
    """
    Функция осуществляет конвертацию суммы каждой транзакции в эквивалент суммы в рублях"
    """
    if not API_KEY:
        raise Exception("API ключ не найден. Установите EXCHANGE_API_KEY в .env файле")

    try:
        amount = float(transaction["operationAmount"]["amount"])
        trans_currency = transaction["operationAmount"]["currency"]["code"]

        if trans_currency != "RUB":
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={trans_currency}&amount={amount}"
            payload: dict = {}
            headers: dict = {"apikey": API_KEY}
            response = requests.request("get", url=url, headers=headers, data=payload)
            result = json.loads(response.text)
            amount_rub = float(result["result"])
            return amount_rub
        else:
            return amount

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при обращении к API: {e}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Ошибка парсинга ответа API: {e}")
