from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


class TestConvertToRub:
    """Тесты для функции convert_to_rub"""

    # Тесты для RUB транзакций
    def test_rub_transaction_float(self):
        """Тест: рублевая транзакция с дробной суммой"""
        transaction = {"amount": 1000.50, "currency": "RUB"}
        result = convert_to_rub(transaction)

        assert result == 1000.50
        assert isinstance(result, float)

    def test_rub_transaction_int(self):
        """Тест: рублевая транзакция с целой суммой"""
        transaction = {"amount": 1000, "currency": "RUB"}
        result = convert_to_rub(transaction)

        assert result == 1000.0
        assert isinstance(result, float)

    def test_rub_transaction_zero(self):
        """Тест: рублевая транзакция с нулевой суммой"""
        transaction = {"amount": 0, "currency": "RUB"}
        result = convert_to_rub(transaction)

        assert result == 0.0

    def test_rub_transaction_negative(self):
        """Тест: рублевая транзакция с отрицательной суммой"""
        transaction = {"amount": -500, "currency": "RUB"}
        result = convert_to_rub(transaction)

        assert result == -500.0

    # Тесты для USD транзакций
    @patch("src.external_api.get_exchange_rate")
    def test_usd_transaction_success(self, mock_rate):
        """Тест: успешная конвертация USD"""
        mock_rate.return_value = 90.5
        transaction = {"amount": 100, "currency": "USD"}

        result = convert_to_rub(transaction)

        assert result == 9050.0
        mock_rate.assert_called_once_with("USD")

    @patch("src.external_api.get_exchange_rate")
    def test_usd_transaction_float_amount(self, mock_rate):
        """Тест: конвертация USD с дробной суммой"""
        mock_rate.return_value = 90.5
        transaction = {"amount": 99.99, "currency": "USD"}

        result = convert_to_rub(transaction)

        assert result == 99.99 * 90.5
        assert round(result, 1) == 9049.10

    @patch("src.external_api.get_exchange_rate")
    def test_usd_transaction_lowercase_currency(self, mock_rate):
        """Тест: USD в нижнем регистре"""
        mock_rate.return_value = 90.5
        transaction = {"amount": 100, "currency": "usd"}

        result = convert_to_rub(transaction)

        assert result == 9050.0
        mock_rate.assert_called_once_with("USD")

    # Тесты для EUR транзакций
    @patch("src.external_api.get_exchange_rate")
    def test_eur_transaction_success(self, mock_rate):
        """Тест: успешная конвертация EUR"""
        mock_rate.return_value = 100.25
        transaction = {"amount": 50, "currency": "EUR"}

        result = convert_to_rub(transaction)

        assert result == 5012.5
        mock_rate.assert_called_once_with("EUR")

    @patch("src.external_api.get_exchange_rate")
    def test_eur_transaction_large_amount(self, mock_rate):
        """Тест: конвертация большой суммы EUR"""
        mock_rate.return_value = 100.25
        transaction = {"amount": 10000, "currency": "EUR"}

        result = convert_to_rub(transaction)

        assert result == 1002500.0

    # Тесты для обработки ошибок
    def test_missing_amount_field(self):
        """Тест: отсутствует поле amount"""
        transaction = {"currency": "USD"}

        with pytest.raises(ValueError, match="Транзакция не содержит поле 'amount'"):
            convert_to_rub(transaction)

    def test_missing_currency_field(self):
        """Тест: отсутствует поле currency"""
        transaction = {"amount": 100}

        with pytest.raises(ValueError, match="Транзакция не содержит поле 'currency'"):
            convert_to_rub(transaction)

    def test_empty_transaction(self):
        """Тест: пустая транзакция"""
        transaction = {}

        with pytest.raises(ValueError, match="Транзакция не содержит поле 'amount'"):
            convert_to_rub(transaction)

    def test_amount_as_string(self):
        """Тест: сумма в виде строки"""
        transaction = {"amount": "100", "currency": "USD"}

        with pytest.raises(ValueError, match="Сумма должна быть числом"):
            convert_to_rub(transaction)

    def test_amount_as_none(self):
        """Тест: сумма равна None"""
        transaction = {"amount": None, "currency": "USD"}

        with pytest.raises(ValueError, match="Сумма должна быть числом"):
            convert_to_rub(transaction)

    def test_amount_as_list(self):
        """Тест: сумма в виде списка"""
        transaction = {"amount": [100], "currency": "USD"}

        with pytest.raises(ValueError, match="Сумма должна быть числом"):
            convert_to_rub(transaction)

    def test_amount_as_dict(self):
        """Тест: сумма в виде словаря"""
        transaction = {"amount": {"value": 100}, "currency": "USD"}

        with pytest.raises(ValueError, match="Сумма должна быть числом"):
            convert_to_rub(transaction)

    def test_unsupported_currency_gbp(self):
        """Тест: неподдерживаемая валюта GBP"""
        transaction = {"amount": 100, "currency": "GBP"}

        with pytest.raises(ValueError, match="Неподдерживаемая валюта: GBP"):
            convert_to_rub(transaction)

    def test_unsupported_currency_cny(self):
        """Тест: неподдерживаемая валюта CNY"""
        transaction = {"amount": 100, "currency": "CNY"}

        with pytest.raises(ValueError, match="Неподдерживаемая валюта: CNY"):
            convert_to_rub(transaction)

    def test_unsupported_currency_jpy(self):
        """Тест: неподдерживаемая валюта JPY"""
        transaction = {"amount": 100, "currency": "JPY"}

        with pytest.raises(ValueError, match="Неподдерживаемая валюта: JPY"):
            convert_to_rub(transaction)

    # Тесты для обработки ошибок API
    @patch("src.external_api.get_exchange_rate")
    def test_api_error_handling_usd(self, mock_rate):
        """Тест: обработка ошибки API для USD"""
        mock_rate.side_effect = Exception("API service unavailable")
        transaction = {"amount": 100, "currency": "USD"}

        with pytest.raises(Exception, match="Ошибка конвертации USD в RUB"):
            convert_to_rub(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_api_error_handling_eur(self, mock_rate):
        """Тест: обработка ошибки API для EUR"""
        mock_rate.side_effect = Exception("Rate limit exceeded")
        transaction = {"amount": 100, "currency": "EUR"}

        with pytest.raises(Exception, match="Ошибка конвертации EUR в RUB"):
            convert_to_rub(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_api_timeout_error(self, mock_rate):
        """Тест: таймаут API"""
        mock_rate.side_effect = Exception("Timeout error")
        transaction = {"amount": 100, "currency": "USD"}

        with pytest.raises(Exception, match="Ошибка конвертации USD в RUB"):
            convert_to_rub(transaction)

    # Интеграционные тесты с моком
    @patch("src.external_api.get_exchange_rate")
    def test_multiple_transactions_same_currency(self, mock_rate):
        """Тест: несколько транзакций с одинаковой валютой"""
        mock_rate.return_value = 90.5

        transactions = [
            {"amount": 100, "currency": "USD"},
            {"amount": 200, "currency": "USD"},
            {"amount": 300, "currency": "USD"},
        ]

        results = [convert_to_rub(t) for t in transactions]

        assert results == [9050.0, 18100.0, 27150.0]
        assert mock_rate.call_count == 3

    @patch("src.external_api.get_exchange_rate")
    def test_mixed_currencies(self, mock_rate):
        """Тест: смешанные валюты"""

        def side_effect(currency):
            return 90.5 if currency == "USD" else 100.25

        mock_rate.side_effect = side_effect

        transactions = [
            {"amount": 100, "currency": "USD"},
            {"amount": 100, "currency": "EUR"},
            {"amount": 100, "currency": "RUB"},
        ]

        results = [convert_to_rub(t) for t in transactions]

        assert results == [9050.0, 10025.0, 100.0]
        assert mock_rate.call_count == 2
        mock_rate.assert_any_call("USD")
        mock_rate.assert_any_call("EUR")
