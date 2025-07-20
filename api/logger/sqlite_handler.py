import sqlite3
import logging
from typing import Any, List, Sequence


class SQLiteHandler(logging.Handler):
    """A logging handler that writes log records to an SQLite database."""

    def __init__(
        self,
        db_path: str,
        table: str,
        columns: Sequence[str],
        ddl: str,
        level: int = logging.INFO,
    ):
        super().__init__(level=level)
        self.db_path = db_path
        self.table = table
        self.columns = list(columns)
        self._ddl = ddl
        self._generate_insert_sql()
        self._ensure_schema()

    def _generate_insert_sql(self) -> str:
        placeholders = ",".join(["?"] * len(self.columns))
        column_list = ",".join(self.columns)
        self._insert_sql = (
            f"INSERT INTO {self.table} ({column_list}) VALUES ({placeholders})"
        )

    def _ensure_schema(self) -> None:
        """Ensure that the database is ready.

        Sets the journal mode to WAL (Write-Ahead Logging). In this mode,
        SQLite allows concurrent reads and writes by appending changes to a
        separate log file before committing them to the main database file.
        This improves performance and concurrency.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.executescript(self._ddl)
            conn.commit()

    def row_from_record(self, record: logging.LogRecord) -> List[Any]:
        """Convert a logging record to a row for insertion into the database.

        Args:
            record (logging.LogRecord): a logging record.

        Returns:
            Sequence[Any]: the row data corresponding to the record.
        """
        return [getattr(record, col, None) for col in self.columns]

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the SQLite database.

        Args:
            record (logging.LogRecord): a logging record.
        """

        try:
            row = self.row_from_record(record)

            if len(row) != len(self.columns):
                raise ValueError(
                    f"Row length ({len(row)}) does not match columns length "
                    f"({len(self.columns)})."
                )

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(self._insert_sql, row)
                conn.commit()
        except Exception:
            self.handleError(record)
