# lib/query_map.py
from pathlib import Path
from typing import Dict

_QUERIES: Dict[str, str] = {}

def load_queries(dir_path: str = "./queries") -> None:
    """-- name: key 블록을 읽어서 {key: sql}로 캐시"""
    base = Path(dir_path)
    for p in base.glob("*.sql"):
        _parse_file(p)

def get_query(key: str) -> str:
    sql = _QUERIES.get(key)
    if not sql:
        raise KeyError(f"Query not found: {key}")
    return sql

def _parse_file(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    cur_key = None
    buf = []

    def flush():
        nonlocal cur_key, buf
        if cur_key and buf:
            # 빈 줄 정리 + 세미콜론 제거(혹시 있을 경우)
            sql = "\n".join(buf).strip().rstrip(";").strip()
            if sql:
                _QUERIES[cur_key] = sql
        cur_key, buf = None, []

    for line in lines:
        if line.strip().lower().startswith("-- key:"):
            flush()
            cur_key = line.split(":", 1)[1].strip()
        else:
            if cur_key is not None:
                buf.append(line)

    flush()