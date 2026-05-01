# from passlib.context import CryptContext
# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBearer
# import jwt
# from datetime import datetime, timezone, timedelta
# from core.config import settings

# pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
# security = HTTPBearer()

# def verify_password(plain_pwd : str, hashed_pwd : str):
#     return pwd.verify(plain_pwd,hashed_pwd)

# def create_access_token(u):
#     return jwt.encode({
#         "sub": u['user_id'],
#         "role": u['role'],
#         "region": u['region'],
#         "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_MIN)
#     }, settings.JWT_SECRET_KEY, algorithm="HS256")

# def create_refresh_token(u):
#     return jwt.encode({
#         "sub": u['user_id'],
#         "role": u['role'],
#         "region": u['region'],
#         "type": "refresh",
#         "exp": datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_DAYS)
#     }, settings.JWT_SECRET_KEY, algorithm="HS256")

# def require_auth(creds=Depends(security)):
#     try:
#         return jwt.decode(creds.credentials, settings.JWT_SECRET_KEY, algorithms=["HS256"])
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

# 비밀번호 암호화 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 토큰을 추출할 URL 설정 (로그인 엔드포인트)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class SecurityHandler:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_password2(plain_password, hashed_password):
        plain_to_hashed_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest();
        return plain_to_hashed_password.lower() == hashed_password.lower()

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None, is_refresh: bool = False):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_MINUTES))
        to_encode.update({"exp": expire, "type": "refresh" if is_refresh else "access"})
        secret = settings.JWT_REFRESH_SECRET_KEY if is_refresh else settings.JWT_SECRET_KEY
        return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)

def require_auth(token: str = Depends(oauth2_scheme)):
    """컨트롤러에서 Depends(require_auth)로 사용"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id} # 필요한 사용자 정보 반환
    except JWTError:
        raise credentials_exception