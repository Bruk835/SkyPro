import pytest


@pytest.fixture
def three_letters_str() -> str:
    return "asa"


@pytest.fixture
def empty_str() -> str:
    return ""


@pytest.fixture
def empty_list() -> list:
    return []


@pytest.fixture
def three_letters_list() -> list:
    return ["asa"]
