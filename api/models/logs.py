from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RequestLogModel(Base):
    __tablename__ = "requests"

    ts = Column(Float, primary_key=True, index=True)
    client_addr = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    path = Column(String, nullable=False)


class AppLogModel(Base):
    __tablename__ = "app_logs"

    ts = Column(Float, primary_key=True, index=True)
    level = Column(String, nullable=False)
    logger = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    lineno = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
