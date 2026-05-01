import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import db_manager
from core.query_loader import QueryLoader
from core.config import settings
from controller import auth_controller
from controller import user_controller
from controller import equip_controller

print("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [Startup] 앱 시작 시 실행
    db_manager.initialize()
    QueryLoader.load_queries()
    print("🚀 Database pool initialized and queries loaded.")
    yield
    # [Shutdown] 앱 종료 시 실행
    db_manager.close()
    print("🛑 Database pool closed.")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

print("app", app)

# Router 등록
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(equip_controller.router)

if __name__ == "__main__":
    # Spring Boot처럼 실행
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)