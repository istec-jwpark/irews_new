from fastapi import FastAPI
from backup.app.router.user import router as user_router
from backup.app.lib.query_map import load_queries
from backup.app.lib.db import init_pool

app = FastAPI()

@app.on_event("startup")
def startup():
    load_queries("app/queries")
    init_pool(user="USER", password="PW", dsn="HOST:1521/SERVICE")

app.include_router(user_router)