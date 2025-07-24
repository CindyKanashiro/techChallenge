from fastapi import FastAPI

import api.routes as routes
from api.logger.setup import setup_logging
from api.routes import scraping

setup_logging("logs.db")

app = FastAPI(title="Books API", version="1.0")

routers = [
    routes.books_router,
    routes.categories_router,
    routes.stats_router,
    routes.health_router,
    routes.auth_router,
]

for router in routers:
    app.include_router(router)

app.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
