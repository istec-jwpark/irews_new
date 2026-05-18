import oracledb
from core.config import settings
from contextlib import asynccontextmanager

""" Async DatabaseManager """
class ADatabaseManager:
    _pool = None

    @classmethod
    async def initialize(cls):
        """앱 시작 시 비동기 풀 초기화"""
        if cls._pool is None:
            # threading=False는 asyncio 환경에서 성능상 유리할 수 있습니다.
            cls._pool = oracledb.create_pool_async(
                user=settings.ORACLE_USER,
                password=settings.ORACLE_PASSWORD,
                dsn=settings.ORACLE_DSN,
                min=settings.DB_POOL_MIN,
                max=settings.DB_POOL_MAX,
                increment=settings.DB_POOL_INC
            )

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        """비동기 트랙션 및 커넥션 관리"""
        conn = await cls._pool.acquire()
        conn.autocommit = False 
        try:
            yield conn
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            raise e
        finally:
            await cls._pool.release(conn)

    @classmethod
    async def close(cls):
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None

db_manager = ADatabaseManager()