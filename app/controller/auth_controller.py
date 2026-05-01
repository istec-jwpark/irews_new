
from fastapi import APIRouter
from service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login_api(param: dict):
    _service = AuthService()
    return _service.login(param["user_id"], param["user_pwd"])

@router.post("/refresh")
def refresh_api(param: dict):
    return AuthService.refresh(param["refresh_token"])
