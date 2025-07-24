import logging

from api.logger.app_log_handler import AppLogHandler
from api.logger.request_log_handler import RequestLogHandler


def setup_logging(db_path: str = "logs.db") -> None:
    """Set up logging handlers for the application.

    Args:
        db_path (str): Path to the SQLite database file.
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Handlers de SQLite
    app_handler = AppLogHandler(db_path=db_path)
    root_logger.addHandler(app_handler)

    request_handler = RequestLogHandler(db_path=db_path)
    # requests_logger = logging.getLogger("requests")
    requests_logger = logging.getLogger("uvicorn.access")
    requests_logger.addHandler(request_handler)

    # Handler de console para debug
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # root_logger.addHandler(console_handler)

    for child_logger in [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "starlette",
        "httpx",
        "sqlalchemy",
        "sqlalchemy.engine",
    ]:
        logging.getLogger(child_logger).propagate = True  # propaga logs pro root
