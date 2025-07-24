from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

BOOKS_DB = "sqlite:///data/books.db"
books_engine = create_engine(
    BOOKS_DB, connect_args={"check_same_thread": False}, echo=False
)
BooksSession = sessionmaker(autocommit=False, autoflush=False, bind=books_engine)

LOGS_DB = "sqlite:///data/logs.db"
logs_engine = create_engine(
    LOGS_DB, connect_args={"check_same_thread": False}, echo=False
)
LogsSession = sessionmaker(autocommit=False, autoflush=False, bind=logs_engine)


def get_books_session() -> Session:
    return BooksSession()


def get_logs_session() -> Session:
    return LogsSession()
