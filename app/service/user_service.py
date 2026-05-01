from core.database import db_manager
from repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_user_info(self, user_id: str):
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. 단일 조회 (공통 메서드 사용)
                user = self.user_repo.find_one(
                    cursor, "find_by_id", {"user_id": user_id}
                )
                return user


    # def get_user_and_update_login(self, user_id: str):
    #     with db_manager.get_connection() as conn:
    #         with conn.cursor() as cursor:
    #             # 1. 단일 조회 (공통 메서드 사용)
    #             user = self.user_repo.find_one(
    #                 cursor, "find_by_id", {"user_id": user_id}
    #             )
                
    #             if user:
    #                 # 2. 수정 (공통 메서드 사용)
    #                 self.user_repo.execute_edit(cursor, "update_last_login", {"user_id": user_id})
                
    #             return user