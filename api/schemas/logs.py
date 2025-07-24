from pydantic import BaseModel, ConfigDict


class RequestLogSchema(BaseModel):
    ts: float
    client_addr: str
    method: str
    status_code: int
    path: str

    model_config = ConfigDict(from_attributes=True)


class AppLogSchema(BaseModel):
    ts: float
    level: str
    logger: str
    filename: str
    lineno: int
    message: str

    model_config = ConfigDict(from_attributes=True)
