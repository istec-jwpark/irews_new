import uvicorn, time
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
# from core.database import db_manager
from core.adatabase import db_manager
from core.query_loader import QueryLoader
from core.service_loader import ServiceLoader
# from core.filter_loader import FilterLoader
from core.config import settings
from core.logger import log_middleware
from api import auth_api
from api import base_api
from api import map_api
from api import equip_api

print("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [Startup] 앱 시작 시 실행
    await db_manager.initialize()
    QueryLoader.load_queries()
    logger.info(QueryLoader.get_query("equip","point_base_list"))
    ServiceLoader.load_services()
    logger.info(ServiceLoader.run("test.test",{"a":"a"}))
    # FilterLoader.load_filter()
    # logger.info(FilterLoader.run("equip","test",{"a":"a"}))
    logger.info("🚀 Database pool initialized, queries/services loaded.")
    yield
    # [Shutdown] 앱 종료 시 실행
    await db_manager.close()
    logger.info("🛑 Database pool closed.")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

## 미들 웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await log_middleware(request, call_next)

origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("app", app)

# Router 등록
app.include_router(auth_api.router)
app.include_router(base_api.router)
# app.include_router(map_api.router)
# app.include_router(equip_api.router)

if __name__ == "__main__":
    # Spring Boot처럼 실행
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, timeout_keep_alive=60)