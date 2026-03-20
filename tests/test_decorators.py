import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


def test_log_in_console(capsys: CaptureFixture[str]) -> None:
    @log()  # type: ignore[call-arg]
    def add_num(a: int, b: int) -> int:
        return a + b

    result = add_num(5, 4)
    assert result == 9
    capture = capsys.readouterr()
    assert "Function add_num status: Ok" in capture.out
    assert "Result: 9" in capture.out


def test_log_error_to_console(capsys: CaptureFixture[str]) -> None:
    """Тест вывода ошибки в консоль"""

    @log()  # type: ignore[call-arg]
    def error_func() -> None:
        raise ValueError("Test error message")
    with pytest.raises(ValueError, match="Test error message"):
        error_func()

    captured = capsys.readouterr()
    expected_error = "Function error_func error: ValueError: Test error message"
    assert expected_error in captured.out
    assert "args=(), kwargs={}" in captured.out


def test_log_error_with_args_to_console(capsys: CaptureFixture[str]) -> None:
    """Тест вывода ошибки с аргументами функции"""

    @log()  # type: ignore[call-arg]
    def divide(a: int, b: int) -> int:
        return a // b
    with pytest.raises(ZeroDivisionError):
        divide(9, 0)

    captured = capsys.readouterr()
    expected = "Function divide error: ZeroDivisionError: division by zero (args=(9, 0), kwargs={})"
    assert expected in captured.out


def test_log_to_file_simple(log_filename: str) -> None:
    """Тест записи в файл для простой функции"""

    @log(filename=log_filename)
    def simple_func() -> str:
        return "Hello World!"

        assert simple_func() == "Hello World!"

        with open(log_filename, "r") as f:
            content = f.read()
            assert "Function simple_func status: Ok" in content
            assert "Result: Hello World!" in content
            assert "Start time:" in content
            assert "Stop time:" in content


def test_log_to_file_with_args(log_filename: str) -> None:
    """Тест записи в файл для функции с аргументами"""

    @log(filename=log_filename)
    def multiply(a: int, b: int) -> int:
        return a * b

        result = multiply(3, 9)

        assert result == 27

        with open(log_filename, "r") as f:
            content = f.read()
            assert "Function multiply status: Ok" in content
            assert "Result: 27" in content


def test_log_to_file_with_different_functions(log_filename: str) -> None:
    """Тест записи разных функций в один файл"""

    @log(filename=log_filename)
    def func1() -> str:
        return "1st"

    @log(filename=log_filename)
    def func2() -> str:
        return "2nd"

    func1()
    func2()

    with open(log_filename, "r") as f:
        content = f.read()
        assert "Function func1 status: Ok" in content
        assert "Function func2 status: Ok" in content
        assert "Result: 1st" in content
        assert "Result: 2nd" in content


def test_log_error_to_file_not_written(log_filename: str, capsys: CaptureFixture[str]) -> None:
    """Тест, что ошибки НЕ записываются в файл (только в консоль)"""

    @log(filename=log_filename)
    def error_func() -> None:
        raise RuntimeError("Test error")

    with pytest.raises(RuntimeError):
        error_func()

    # Проверяем, что файл пустой (ошибки не записались)
    with open(log_filename, "r") as f:
        content = f.read()
        assert content == ""  # Файл должен быть пустым

    # Проверяем, что ошибка была в консоли
    captured = capsys.readouterr()
    assert "Function error_func error: RuntimeError: Test error" in captured.out
