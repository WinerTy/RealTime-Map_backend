from .logger import GunicornLogger


def get_application_options(
    bind: str, timeout: int, workers: int, log_level: str
) -> dict:
    return {
        "accesslog": "-",
        "errorlog": "-",
        "loglevel": log_level,
        "logger_class": GunicornLogger,
        "bind": bind,
        "workers": workers,
        "timeout": timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
