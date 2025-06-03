from typing import Callable, Any, Tuple, Dict

from fastapi import Request, Response


def custom_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Request,
    response: Response,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    kwargs_for_key = kwargs.copy() if kwargs else {}

    if "repo" in kwargs_for_key:
        del kwargs_for_key["repo"]

    print(args)
    print(kwargs_for_key)
    cache_key = (
        namespace
        + f":{func.__module__}:{func.__name__}"
        + f":{args}"
        + f":{sorted(kwargs_for_key.items())}"
    )
    return cache_key
