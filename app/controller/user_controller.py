
from fastapi import APIRouter, Depends
from service.user_service import UserRepository
from util.security import require_auth

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(p: dict):
    return UserRepository.get_user_info(p['user_id'])


# @router.get("/me")
# def me(user = Depends(require_auth)):
#     return UserRepository.get_user_info(user)