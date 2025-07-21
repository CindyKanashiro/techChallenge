import logging
from api.logger.sqlite_handler import SQLiteHandler


class AppLogHandler(SQLiteHandler):
    """Handler for logging application events to an SQLite database."""

    _DDL = """
    CREATE TABLE IF NOT EXISTS app_logs (
        ts       REAL,
        level    TEXT,
        logger   TEXT,
        filename TEXT,
        lineno   INTEGER,
        message  TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_app_logs_ts ON app_logs(ts);
    """

    def __init__(self, db_path: str = "log.db", level: int = logging.INFO):
        super().__init__(
            db_path=db_path,
            table="app_logs",
            columns=[
                "ts",
                "level",
                "logger",
                "filename",
                "lineno",
                "message",
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
        return [
            record.created,
            record.levelname,
            record.name,
            record.pathname,
            record.lineno,
            record.getMessage(),
        ]
