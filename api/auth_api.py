from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger
from core.jwt_handler import create_access_token, verify_password, verify_password_simple
from passlib.context import CryptContext

# 가상의 유저 데이터베이스 (실제로는 DB에서 조회)
fake_users_db = {
    "admin_user": {
        "username": "admin_user",
        # 비밀번호 'secret123'의 bcrypt 해시값
        "hashed_password": "7b3d979ca8330a94fa7e9e1b466d8b99e0bcdea1ec90596c0dcc8d7ef6b4300c",#pwd_context.hash("test"), 
    }
}
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 1. 유저 존재 여부 확인
    user = fake_users_db.get(form_data.username)
    if not user:
        logger.warning(f"Login failed: User {form_data.username} not found.")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 비밀번호 검증
    if not verify_password_simple(form_data.password, user["hashed_password"]):
        logger.warning(f"Login failed: Incorrect password for user {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 로그인 성공 로그 (7일 보관 로그 파일에 기록됨)
    logger.success(f"User {form_data.username} logged in successfully.")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}