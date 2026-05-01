from typing import List, Dict, Any, Optional
from core.query_loader import QueryLoader
from core.query_executor import QueryExecutor

class BaseRepository:
    def __init__(self, category: str):
        self.category = category

    def _get_sql(self, query_id: str) -> str:
        sql = QueryLoader.get(self.category, query_id)
        print("****** QUERY ID : ", query_id)
        print(sql)
        if not sql:
            raise ValueError(f"Query ID '{query_id}' not found in category '{self.category}'")
        return sql

    def find_one(self, cursor, query_id: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        return QueryExecutor.fetch_one(cursor, self._get_sql(query_id), params)

    def find_list(self, cursor, query_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        return QueryExecutor.fetch_all(cursor, self._get_sql(query_id), params)

    def execute_edit(self, cursor, query_id: str, params: Dict[str, Any] = None) -> int:
        """입력, 수정, 삭제 공통 (affected rows 반환)"""
        return QueryExecutor.execute(cursor, self._get_sql(query_id), params)