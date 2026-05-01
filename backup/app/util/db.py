# lib/db.py
import oracledb

POOL = None

def init_pool(user: str, password: str, dsn: str, min=1, max=5, inc=1):
    global POOL
    POOL = oracledb.create_pool(
        user=user,
        password=password,
        dsn=dsn,
        min=min,
        max=max,
        increment=inc,
    )

def get_conn():
    if POOL is None:
        raise RuntimeError("DB pool not initialized")
    return POOL.acquire()