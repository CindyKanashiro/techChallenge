from api.logger.sqlite_handler import SQLiteHandler
import logging


class RequestLogHandler(SQLiteHandler):
    """Handler for logging HTTP request data to an SQLite database."""

    _DDL = """
    CREATE TABLE IF NOT EXISTS requests (
        ts          REAL,
        client_addr TEXT,
        method      TEXT,
        status_code INTEGER,
        duration_ms REAL
    );
    CREATE INDEX IF NOT EXISTS idx_requests_ts ON requests(ts);
    """

    def __init__(self, db_path: str = "log.db", level: int = logging.INFO):
        super().__init__(
            db_path=db_path,
            table="requests",
            columns=[
                "ts",
                "client_addr",
                "method",
                "status_code",
                "duration_ms",
            ],
            ddl=self._DDL,
            level=level,
        )
