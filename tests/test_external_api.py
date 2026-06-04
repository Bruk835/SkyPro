import json
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import amount_in_rub


def test_amount_in_rub_with_rub_currency():
    """Тест для транзакции в рублях (конвертация не требуется)"""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }

    result = amount_in_rub(transaction)
    assert result == 100.50
    assert isinstance(result, float)


def test_amount_in_rub_with_integer_amount():
    """Тест с целым числом в рублях"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "RUB"}
        }
    }

    result = amount_in_rub(transaction)
    assert result == 100.0


@patch('src.external_api.requests.request')
def test_amount_in_rub_usd_to_rub(mock_request):
    """Тест конвертации USD в RUB"""
    # Мокаем успешный ответ API
    mock_response = Mock()
    mock_response.text = json.dumps({"result": 7500.50})
    mock_request.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    # Патчим переменную API_KEY, чтобы она была доступна
    with patch('src.external_api.API_KEY', 'test_api_key'):
        result = amount_in_rub(transaction)

    assert result == 7500.50

    # Проверяем, что API был вызван с правильными параметрами
    mock_request.assert_called_once()
    call_args = mock_request.call_args
    assert call_args[1]['url'].startswith('https://api.apilayer.com/exchangerates_data/convert')
    assert 'to=RUB' in call_args[1]['url']
    assert 'from=USD' in call_args[1]['url']
    assert 'amount=100' in call_args[1]['url']


@patch('src.external_api.requests.request')
def test_amount_in_rub_eur_to_rub(mock_request):
    """Тест конвертации EUR в RUB"""
    mock_response = Mock()
    mock_response.text = json.dumps({"result": 9200.75})
    mock_request.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "EUR"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        result = amount_in_rub(transaction)

    assert result == 9200.75


@patch('src.external_api.requests.request')
def test_amount_in_rub_with_decimal_amount(mock_request):
    """Тест конвертации с десятичной суммой"""
    mock_response = Mock()
    mock_response.text = json.dumps({"result": 373.25})
    mock_request.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "5.50",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        result = amount_in_rub(transaction)

    assert result == 373.25


def test_amount_in_rub_no_api_key():
    """Тест: отсутствие API ключа должно вызывать исключение"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', None):
        with pytest.raises(Exception, match="API ключ не найден"):
            amount_in_rub(transaction)


@patch('src.external_api.requests.request')
def test_amount_in_rub_api_request_error(mock_request):
    """Тест: ошибка при запросе к API"""
    # Выбрасываем именно RequestException, а не обычное Exception
    mock_request.side_effect = requests.exceptions.RequestException("Connection error")

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(Exception, match="Ошибка при обращении к API"):
            amount_in_rub(transaction)


@patch('src.external_api.requests.request')
def test_amount_in_rub_invalid_json_response(mock_request):
    """Тест: API вернул некорректный JSON"""
    mock_response = Mock()
    mock_response.text = "invalid json"
    mock_request.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(Exception, match="Ошибка парсинга ответа API"):
            amount_in_rub(transaction)


@patch('src.external_api.requests.request')
def test_amount_in_rub_missing_result_field(mock_request):
    """Тест: в ответе API отсутствует поле 'result'"""
    mock_response = Mock()
    mock_response.text = json.dumps({"error": "Invalid currency"})
    mock_request.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(Exception, match="Ошибка парсинга ответа API"):
            amount_in_rub(transaction)


def test_amount_in_rub_missing_currency_field():
    """Тест: в транзакции отсутствует поле currency"""
    transaction = {
        "operationAmount": {
            "amount": "100"
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(Exception, match="Ошибка парсинга ответа API"):
            amount_in_rub(transaction)


def test_amount_in_rub_invalid_amount_format():
    """Тест: сумма транзакции в некорректном формате"""
    transaction = {
        "operationAmount": {
            "amount": "not_a_number",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.API_KEY', 'test_api_key'):
        with pytest.raises(Exception, match="Ошибка парсинга ответа API"):
            amount_in_rub(transaction)


@patch('src.external_api.requests.request')
def test_amount_in_rub_with_different_currencies(mock_request):
    """Тест конвертации разных валют"""

    # Создаем разные ответы для разных вызовов
    def mock_api_call(*args, **kwargs):
        mock_resp = Mock()
        if 'from=USD' in kwargs['url']:
            mock_resp.text = json.dumps({"result": 7500.00})
        elif 'from=EUR' in kwargs['url']:
            mock_resp.text = json.dumps({"result": 8800.00})
        else:
            mock_resp.text = json.dumps({"result": 500.00})
        return mock_resp

    mock_request.side_effect = mock_api_call

    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "100", "currency": {"code": "EUR"}}},
    ]

    with patch('src.external_api.API_KEY', 'test_api_key'):
        results = [amount_in_rub(t) for t in transactions]

    assert results[0] == 7500.00
    assert results[1] == 8800.00
    assert mock_request.call_count == 2