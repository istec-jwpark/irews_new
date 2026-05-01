
# import jwt
# from util.security import verify_password, create_access_token, create_refresh_token
# from core.config import settings
# from core.database import db_manager
# from repository.auth_repository import AuthRepository as Repository

# def login(user_id, password):
#     repo = Repository()
#     _user = repo.find_user(user_id)
#     print("###### login ######")
#     print(_user)
#     if not _user or not verify_password(password, _user['user_pwd']):
#         raise ValueError("Invalid credentials")
#     return {
#         "access_token": create_access_token(_user),
#         "refresh_token": create_refresh_token(_user),
#         "token_type": "bearer"
#     }
# def refresh(token):
#     payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
#     return {"access_token": create_access_token(payload)}

# class AuthService:
#     def __init__(self):
#         self._repo = Repository()

#     def login(self, user_id:str, user_pwd:str):
#         print("###### login ######")
#         with db_manager.get_connection() as conn:
#             with conn.cursor() as cursor:
#                 # 1. 단일 조회 (공통 메서드 사용)
#                 result = self._repo.find_one(
#                     cursor, "find_user", {"user_id": user_id}
#                 )
#                 print(result)
#                 if not result or not verify_password(user_pwd, result['user_pwd']):
#                     raise ValueError("Invalid credentials")
#                 return {
#                     "access_token": create_access_token(result),
#                     "refresh_token": create_refresh_token(result),
#                     "token_type": "bearer"
#                 }

#     @classmethod
#     def refresh(token):
#         payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
#         return {"access_token": create_access_token(payload)}

from core.database import db_manager
from repository.auth_repository import AuthRepository
from util.security import SecurityHandler
from fastapi import HTTPException

class AuthService:
    def __init__(self):
        self._repo = AuthRepository()

    def login(self, user_id, user_pwd):
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                user = self._repo.find_one(cursor, "find_user", {"user_id": user_id})
                # DB 비밀번호와 입력 비밀번호 검증 (실제론 해시 비교)
                valid_user = SecurityHandler.verify_password2(user_pwd, user['user_pwd'])
                print(user, valid_user)
                if not user: # or user['user_pwd'] != user_pwd:
                    raise HTTPException(status_code=401, detail="Invalid ID or Password")

                access_token = SecurityHandler.create_token(data={"sub": user_id})
                refresh_token = SecurityHandler.create_token(data={"sub": user_id}, is_refresh=True)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer"
                }