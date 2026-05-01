from core.database import db_manager
from repository.equip_repository import EquipRepository

class EquipService:
    def __init__(self):
        self._repo = EquipRepository()

    def rsvr_list_by_site_sq(self, site_sq: str):
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. 단일 조회 (공통 메서드 사용)
                result = self._repo.find_list(
                    cursor, "rsvr_list_by_site_sq", {"site_sq": site_sq}
                )
                return result