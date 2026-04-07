from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import API_KEY, BASE_URL, get_exchange_rate


class TestGetExchangeRate:
    """Тесты для функции get_exchange_rate"""

    @patch("src.external_api.requests.get")
    def test_successful_usd_rate(self, mock_get):
        """Тест: успешное получение курса USD"""
        # Подготовка мока
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 90.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызов функции
        rate = get_exchange_rate("USD")

        # Проверки
        assert rate == 90.5
        assert isinstance(rate, float)
        mock_get.assert_called_once()

        # Проверка параметров запроса
        call_args = mock_get.call_args
        assert call_args[1]["headers"]["apikey"] == API_KEY
        assert call_args[1]["params"]["from"] == "USD"
        assert call_args[1]["params"]["to"] == "RUB"
        assert call_args[1]["params"]["amount"] == 1

    @patch("src.external_api.requests.get")
    def test_successful_eur_rate(self, mock_get):
        """Тест: успешное получение курса EUR"""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 100.25}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("EUR")

        assert rate == 100.25
        assert isinstance(rate, float)

        # Проверка параметров запроса
        call_args = mock_get.call_args
        assert call_args[1]["params"]["from"] == "EUR"

    @patch("src.external_api.requests.get")
    def test_case_insensitive_currency(self, mock_get):
        """Тест: регистронезависимость кода валюты"""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 90.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("usd")  # нижний регистр

        assert rate == 90.5
        # Проверяем, что в запрос ушел USD в верхнем регистре
        call_args = mock_get.call_args
        assert call_args[1]["params"]["from"] == "USD"
