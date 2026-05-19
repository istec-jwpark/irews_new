from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger
from core.abase_service import AService as Service
from core.jwt_handler import create_access_token, verify_password_simple, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 1. 유저 존재 여부 확인
    _user_id = form_data.username
    _user_pwd = form_data.password
    _service = Service()
    params = {'user_id':_user_id}
    _result = await _service.find_one('auth','auth_info',params)
    _user_info = None
    if _result['success']:
        _user_info = _result['data']
    logger.info(f'****** DB User Info({_user_id}) : {_user_info}')
    if not _user_info:
        logger.warning(f"Login failed: User {_user_id} not found.")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 비밀번호 검증
    if not verify_password_simple(_user_pwd, _user_info["userPwd"]):
        logger.warning(f"Login failed: Incorrect password for user {_user_id}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 로그인 성공 로그 (7일 보관 로그 파일에 기록됨)
    logger.success(f"User {_user_id} logged in successfully.")
    # 토큰 생성시 사용할 정보 ?
    token_data = {'sub':'test', **{k:v for k,v in _user_info.items() if k != 'userPwd'}}
    access_token = create_access_token(data={"sub": _user_info["userId"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_me(user_id: str = Depends(get_current_user)):
    _service = Service()
    params = {'user_id':user_id}
    _user_info = await _service.find_one('user','get_user',params)
    logger.info(f'****** DB User Info({user_id}) : {_user_info}')
    return _user_info
