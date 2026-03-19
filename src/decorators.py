from functools import wraps
from typing import Any, Callable
from time import time

def log(filename: str=None) -> Callable[]:
    def decorator(func)-> Callable[]:
        @wraps(func)
        def wrappers(*args: Any, **kwargs: Any)-> Any:
            try:
                start_time = time()
                result = func(*args, **kwargs)
                stop_time = time()
                if filename:
                    with open(filename, "a") as f:
                        f.write(
                            f"Функция {func.__name__}: Ok,\n"
                            f"результат: {result},\n"
                            f"время начала работы функции:{start_time},\n"
                            f"время окончания работы функции:{stop_time}.\n")
                else:
                    print(
                        f"Функция {func.__name__}: Ok,\n"
                        f"результат: {result},\n"
                        f"время начала работы функции:{start_time},\n"
                        f"время окончания работы функции:{stop_time}.\n")
            except Exception as e:
                print(f"Функция {func.__name__} error: {type(e).__name__}: {e} (args={args}, kwargs={kwargs})\n")
                raise
            return result
        return wrappers
    return decorator
