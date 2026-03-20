from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    def decorator(func: Any) -> Callable:
        @wraps(func)
        def wrappers(*args: Any, **kwargs: Any) -> Any:

            try:
                start_time = datetime.now()
                result = func(*args, **kwargs)
                stop_time = datetime.now()
                if filename:
                    with open(filename, "a") as f:
                        f.write(
                            f"Function {func.__name__} status: Ok\n"
                            f"Result: {result}\n"
                            f"Start time:{start_time}\n"
                            f"Stop time:{stop_time}\n"
                        )
                else:
                    print(
                        f"Function {func.__name__} status: Ok\n"
                        f"Result: {result}\n"
                        f"Start time:{start_time}\n"
                        f"Stop time:{stop_time}\n"
                    )
            except Exception as e:
                print(f"Function {func.__name__} error: {type(e).__name__}: {e} (args={args}, kwargs={kwargs})\n")
                raise
            return result

        return wrappers

    return decorator
