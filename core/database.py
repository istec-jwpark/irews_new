import oracledb
from core.config import settings
from contextlib import contextmanager

class DatabaseManager:
    _pool = None

    @classmethod
    def initialize(cls):
        """앱 시작 시 풀 초기화 (main.py에서 호출)"""
        if cls._pool is None:
            cls._pool = oracledb.create_pool(
                user=settings.ORACLE_USER,
                password=settings.ORACLE_PASSWORD,
                dsn=settings.ORACLE_DSN,
                min=settings.DB_POOL_MIN,
                max=settings.DB_POOL_MAX,
                increment=settings.DB_POOL_INC
            )

    @classmethod
    @contextmanager
    def get_connection(cls):
        """트랜잭션 및 커넥션 관리 컨텍스트 매니저"""
        conn = cls._pool.acquire()
        conn.autocommit = False  # 명시적 트랜잭션 처리를 위해 False
        print("###### get connection ######")
        print(conn)
        try:
            yield conn
            conn.commit()  # 성공 시 커밋
        except Exception as e:
            conn.rollback() # 에러 시 롤백
            raise e
        finally:
            cls._pool.release(conn)

    @classmethod
    def close(cls):
        if cls._pool is not None:
            cls._pool.close()
            cls._pool = None

db_manager = DatabaseManager()