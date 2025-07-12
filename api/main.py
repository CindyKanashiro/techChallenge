from fastapi import FastAPI, Request
import time
import logging
import json

from api.routes.health import router as health_router
from api.routes.books import router as books_router

from api.db import init_db, insert_metric

app = FastAPI(
    title="API Health & Metrics",
    version="1.0.0"
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(books_router, prefix="/api/v1")


# Inicializa o banco SQLite
init_db()

# Logger JSON
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(json.dumps({
    "time": "%(asctime)s",
    "level": "%(levelname)s",
    "message": "%(message)s"
}))
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler("api.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



@app.middleware("http")
async def log_and_store_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    method = request.method
    path = request.url.path
    status_code = response.status_code
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Salvar no banco
    insert_metric(timestamp, method, path, status_code, duration)

    # Log estruturado
    log_data = {
        "time": timestamp,
        "method": method,
        "path": path,
        "status_code": status_code,
        "process_time_ms": round(duration * 1000, 2)
    }
    logger.info(json.dumps(log_data))

    return response
