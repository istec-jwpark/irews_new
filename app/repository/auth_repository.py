from repository.base_repository import BaseRepository

class AuthRepository(BaseRepository):
    def __init__(self):
        # YAML의 'user_queries' 섹션을 사용하도록 설정
        super().__init__("auth_queries")

    # 필요 시 추가적인 특화 로직만 작성
    # 공통 기능은 이미 부모 클래스에 find_one, find_list 등으로 존재함
    def test_user():
        return {
            "group_sq": "1",
            "site_sq": "1",
            "user_sq": "1",
            "user_id": "test",
            "user_pwd":"",
            "role_cd":"1",
            "user_nm":"test"
        }
