from fastapi import FastAPI

import api.routes as routes
from api.logger.setup import setup_logging

setup_logging("data/logs.db")

app = FastAPI(title="Books API", version="1.0")

routers = [
    routes.books_router,
    routes.categories_router,
    routes.stats_router,
    routes.health_router,
    routes.auth_router,
    routes.scraping_router,
]

for router in routers:
    app.include_router(router)
