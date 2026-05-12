import jwt, hashlib
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext

# 실제로는 env에서 가져올 것
SECRET_KEY = "your-ultra-secure-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        # PyJWT 최신 버전은 decode 시 options나 algorithms 설정이 엄격함
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("No user id in token")
        return username
    except jwt.ExpiredSignatureError:
        logger.warning("Expired token access attempt")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError as e:
        logger.error(f"Auth failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_password_hash(password: str):
    """
    비밀번호가 72바이트를 초과하면 로그를 남기고 SHA-256으로 변환합니다.
    """
    pw_bytes = password.encode('utf-8')
    if len(pw_bytes) > 72:
        # 보안을 위해 비밀번호 원문은 절대 로그에 담지 않습니다.
        logger.warning(f"Long password detected ({len(pw_bytes)} bytes). Applying SHA-256 preprocessing.")
        return hashlib.sha256(pw_bytes).hexdigest()
    return password

def verify_password(plain_password: str, hashed_password: str):
    """
    기존 Bcrypt 데이터와 신규 SHA-256 방식을 모두 지원합니다.
    """
    # 1. 먼저 입력값을 전처리(긴 경우 SHA-256)하여 검증 시도
    processed_pw = get_password_hash(plain_password)
    logger.info(plain_password,processed_pw)#,pwd_context.hash(processed_pw))
    try:
        return pwd_context.verify(processed_pw, hashed_password)
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return False
    
def verify_password_simple(plain_password: str, hashed_password: str):
    """ 기존 단순 SHA-256 방식 """
    # 1. 사용자가 입력한 password를 단순 SHA-256으로 변환 후 비교
    # input_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    # 두번 해싱하는 로직으로 변경
    first_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    input_hash = hashlib.sha256(first_hash.encode()).hexdigest()
    if input_hash == hashed_password:
        logger.success("비밀번호 일치 (SHA-256)")
        return True
    
    logger.warning("비밀번호 불일치")
    return False