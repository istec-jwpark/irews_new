from typing import List, Dict, Any, Optional
from core.database import db_manager
from core.query_loader import QueryLoader
from core.query_executor import QueryExecutor

class Service:
    def _get_sql(self, category: str, query_id: str) -> str:
        sql = QueryLoader.get(category, query_id)
        print("****** QUERY ID : ", query_id)
        print(sql)
        if not sql:
            raise ValueError(f"Query ID '{query_id}' not found in category '{self.category}'")
        return sql

    def find_one(self, category: str, query_id: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                return QueryExecutor.fetch_one(cursor, self._get_sql(category,query_id), params)

    def find_list(self, category: str, query_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                return QueryExecutor.fetch_all(cursor, self._get_sql(category, query_id), params)

    def do_execute(self, category: str, query_id: str, params: Dict[str, Any] = None) -> int:
        """입력, 수정, 삭제 공통 (affected rows 반환)"""
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                return QueryExecutor.execute(cursor, self._get_sql(category, query_id), params)