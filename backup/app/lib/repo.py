# lib/repo.py
from typing import Any, Dict, List, Optional
from backup.app.lib.db import get_conn

def select_one(sql: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)  # 바인드 변수 사용 [1](https://python-oracledb.readthedocs.io/en/latest/user_guide/sql_execution.html)
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0].lower() for d in cur.description]
        return dict(zip(cols, row))

def select_all(sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    params = params or {}
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        cols = [d[0].lower() for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def execute(sql: str, params: Dict[str, Any]) -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount