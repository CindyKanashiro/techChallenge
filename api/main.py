from pathlib import Path
from fastapi import FastAPI

import api.routes as routes
from api.logger.setup import setup_logging
from scraping.books import download_catalogue_data

Path('data').mkdir(exist_ok=True)
setup_logging("data/logs.db")
download_catalogue_data()

app = FastAPI(title="Books API", version="1.0")

routers = [
    routes.books_router,
    routes.categories_router,
    routes.stats_router,
    routes.health_router,
    routes.auth_router,
    routes.scraping_router,
    routes.logs_router,
    routes.ml_router,
]

for router in routers:
    app.include_router(router)
