import json
from typing import Any

from src.utils import load_transactions


def test_load_transactions() -> Any:
    """Тестирование функции load_transactions"""

    # 1. Тест с корректным файлом
    with open("test_valid.json", "w", encoding="utf-8") as f:
        json.dump([{"id": 1, "amount": 100}], f)

    result = load_transactions("test_valid.json")
    assert result == [{"id": 1, "amount": 100}]

    # 2. Тест с несуществующим файлом
    result = load_transactions("not_exist.json")
    assert result == []

    # 3. Тест с пустым файлом
    open("test_empty.json", "w").close()
    result = load_transactions("test_empty.json")
    assert result == []

    # 4. Тест с файлом, содержащим не список
    with open("test_dict.json", "w", encoding="utf-8") as f:
        json.dump({"key": "value"}, f)

    result = load_transactions("test_dict.json")
    assert result == []

    # 5. Тест с невалидным JSON
    with open("test_invalid.json", "w", encoding="utf-8") as f:
        f.write("{invalid}")

    result = load_transactions("test_invalid.json")
    assert result == []
