from fastapi import APIRouter
from backup.app.service.rsvr_service import create_user, get_user, list_users

router = APIRouter(prefix="/users", tags=["users"])

@router.post("")
def create(payload: dict):
    return create_user(payload["user_id"], payload["user_name"])

@router.get("/{user_id}")
def get(user_id: str):
    return get_user(user_id)

@router.get("")
def list_():
    return list_users()