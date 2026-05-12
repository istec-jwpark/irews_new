from typing import List, Dict, Any, Optional

class QueryExecutor:
    @staticmethod
    def fetch_one(cursor, sql: str, params: dict = None) -> Optional[Dict[str, Any]]:
        cursor.execute(sql, params or {})
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    @staticmethod
    def fetch_all(cursor, sql: str, params: dict = None) -> List[Dict[str, Any]]:
        cursor.execute(sql, params or {})
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def execute(cursor, sql: str, params: dict = None) -> int:
        cursor.execute(sql, params or {})
        return cursor.rowcount