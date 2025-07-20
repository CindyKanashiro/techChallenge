from api.logger.sqlite_handler import SQLiteHandler
import logging


class RequestLogHandler(SQLiteHandler):
    """Handler for logging HTTP request data to an SQLite database."""

    _DDL = """
    CREATE TABLE IF NOT EXISTS requests (
        ts          REAL,
        client_addr TEXT,
        method      TEXT,
        status_code INTEGER
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
            ],
            ddl=self._DDL,
            level=level,
        )

    def row_from_record(self, record: logging.LogRecord) -> list:
        """Convert a logging record to a row for insertion into the database.

        Args:
            record (logging.LogRecord): a logging record.

        Returns:
            list: the row data corresponding to the record.
        """
        client_addr, method, _path, _http_ver, status_code = record.args
        return [
            record.created,
            client_addr,
            method,
            int(status_code),
        ]
