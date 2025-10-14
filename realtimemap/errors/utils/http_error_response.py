from typing import Type

from errors.base import BaseRealTimeMapException


def http_error_response_generator(
    *exceptions: Type[BaseRealTimeMapException],
) -> dict:
    responses = {}

    for exc in exceptions:
        instance = exc()
        status_code = instance.status_code
        detail = instance.detail

        responses[status_code] = {
            "description": detail,
            "model": instance.response_model,
        }

    return responses
