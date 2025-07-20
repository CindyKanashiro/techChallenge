import logging
from api.logger.sqlite_handler import SQLiteHandler


class AppLogHandler(SQLiteHandler):
    """Handler for logging application events to an SQLite database."""

    _DDL = """
    CREATE TABLE IF NOT EXISTS app_logs (
        ts       REAL,
        level    TEXT,
        logger   TEXT,
        message  TEXT,
        filename TEXT,
        lineno   INTEGER
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
