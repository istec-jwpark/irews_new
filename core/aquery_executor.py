import oracledb
from typing import List, Dict, Any, Optional
from loguru import logger

""" Async QueryExecutor """
class AQueryExecutor:
    @staticmethod
    async def fetch_one(cursor, sql: str, params: dict = None) -> Dict[str, Any]:
        try:
            await cursor.execute(sql, params or {})
            columns = [col[0] for col in cursor.description]
            row = await cursor.fetchone()
            # return dict(zip(columns, rows)) if rows else None
            return {
                "success": True,
                "data": dict(zip(columns, row)) if row else None,
                "error": None
            }
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            logger.error(f"SQL Error [fetch_one]: {error_obj.message} | Query: {sql} | Params: {params}")
            raise
            # return {
            #     "success": False,
            #     "data": None,
            #     "error": {
            #         "code": getattr(error_obj, 'code', 'DPY-ERROR'),
            #         "message": error_obj.message,
            #         "detail": "SQL 바인드 변수와 파라미터가 일치하지 않습니다." if "DPY-4008" in error_obj.message else None
            #     }
            # }
        except Exception as e:
            logger.error(f"Unexpected Error [fetch_one]: {str(e)}")
            raise
            # return {
            #     "success": False,
            #     "data": None,
            #     "error": {"code": "SYSTEM_ERROR", "message": str(e)}
            # }

    @staticmethod
    async def fetch_all(cursor, sql: str, params: dict = None) -> Dict[str, Any]:
        try:
            await cursor.execute(sql, params or {})
            # 결과 컬럼 정보 추출
            columns = [col[0] for col in cursor.description]
            rows = await cursor.fetchall()
            # return [dict(zip(columns, row)) for row in rows]
            return {
                "success": True,
                "data": [dict(zip(columns, row)) for row in rows],
                "error": None
            }
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            # ORA-01008 (바인드 변수 미지정) 등 파라미터 관련 오류 상세 기록
            logger.error(f"SQL Error [fetch_all]: {error_obj.message} (Code: {error_obj.code})")
            logger.debug(f"Failed Query: {sql} | Params: {params}")
            raise
            # return {
            #     "success": False,
            #     "data": [],
            #     "error": {
            #         "code": getattr(error_obj, 'code', 'DPY-ERROR'),
            #         "message": error_obj.message,
            #         "detail": "SQL 바인드 변수와 파라미터가 일치하지 않습니다." if "DPY-4008" in error_obj.message else None
            #     }
            # }
        except Exception as e:
            logger.error(f"Unexpected Error [fetch_all]: {str(e)}")
            raise
            # return {
            #     "success": False,
            #     "data": [],
            #     "error": {"code": "SYSTEM_ERROR", "message": str(e)}
            # }

    @staticmethod
    async def execute(cursor, sql: str, params: dict = None) -> Dict[str, Any]:
        try:
            await cursor.execute(sql, params or {})
            # return cursor.rowcount
            return {
                "success": True,
                "data": cursor.rowcount,
                "error": None
            }
        except oracledb.IntegrityError as e:
            # 제약 조건 위반 (PK 중복, 대시보드 관리 모듈에서 빈번) 처리
            error_obj, = e.args
            logger.warning(f"Integrity Error: {str(e)}")
            raise
            # return {
            #     "success": False,
            #     "data": 0,
            #     "error": {
            #         "code": getattr(error_obj, 'code', 'DPY-ERROR'),
            #         "message": error_obj.message,
            #         "detail": f"Integrity Error: {str(e)}"
            #     }
            # }
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            logger.error(f"Execution Error: {error_obj.message}")
            raise
            # return {
            #     "success": False,
            #     "data": 0,
            #     "error": {
            #         "code": getattr(error_obj, 'code', 'DPY-ERROR'),
            #         "message": error_obj.message,
            #         "detail": "SQL 바인드 변수와 파라미터가 일치하지 않습니다." if "DPY-4008" in error_obj.message else None
            #     }
            # }