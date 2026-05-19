import oracledb
import inspect
from typing import List, Dict, Any, Optional
from loguru import logger
from core.adatabase import db_manager
from core.query_loader import QueryLoader
from core.service_loader import ServiceLoader
from core.aquery_executor import AQueryExecutor

""" Async Service """
class AService:
    def _get_sql(self, category: str, query_id: str) -> str:
        sql = QueryLoader.get_query(category, query_id)
        logger.info(f"****** QUERY Category/ID : {category}/{query_id}")
        logger.info(sql)
        if not sql:
            raise ValueError(f"Query ID '{query_id}' not found in category '{category}'")
        return sql
    async def find_one(self, category: str, query_id: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        logger.info(f"****** params : {params}")
        async with db_manager.get_connection() as conn:
            async with conn.cursor() as cursor:
                return await AQueryExecutor.fetch_one(cursor, self._get_sql(category,query_id), params)

    async def find_list(self, category: str, query_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            async with db_manager.get_connection() as conn:
                async with conn.cursor() as cursor:
                    _type = QueryLoader.get_type(category, query_id)
                    if _type == 'def':
                        _def = QueryLoader.get_def(category, query_id)
                        _service = ServiceLoader.get(_def.strip())
                        if _service:
                            # 동적 로딩 함수가 비동기인 경우와 동기인 경우를 구분하여 호출 필요
                            if inspect.iscoroutinefunction(_service):
                                _sql, _params = await _service(params)
                            else:
                                _sql, _params = _service(params)
                            return await AQueryExecutor.fetch_all(cursor, _sql, _params)
                    return await AQueryExecutor.fetch_all(cursor, self._get_sql(category, query_id), params)
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            # ORA-01008 (바인드 변수 미지정) 등 파라미터 관련 오류 상세 기록
            logger.error(f"Failed API: ~/{category}/{query_id} | Params: {params}")
            logger.error(f"SQL Error [find_list]: {error_obj.message} (Code: {error_obj.code})")
            # raise
            return {
                "success": False,
                "data": [],
                "error": {
                    "code": getattr(error_obj, 'code', 'DPY-ERROR'),
                    "message": error_obj.message,
                    "detail": "SQL 바인드 변수와 파라미터가 일치하지 않습니다." if "DPY-4008" in error_obj.message else None
                }
            }
        except Exception as e:
            logger.error(f"Failed API: ~/{category}/{query_id} | Params: {params}")
            logger.error(f"Unexpected Error [find_list]: {str(e)}")
            # raise
            return {
                "success": False,
                "data": [],
                "error": {"code": "SYSTEM_ERROR", "message": str(e)}
            }

    async def do_execute(self, category: str, query_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            async with db_manager.get_connection() as conn:
                async with conn.cursor() as cursor:
                    return await AQueryExecutor.execute(cursor, self._get_sql(category, query_id), params)
        except oracledb.IntegrityError as e:
            # 제약 조건 위반 (PK 중복, 대시보드 관리 모듈에서 빈번) 처리
            error_obj, = e.args
            logger.error(f"Failed API: ~/{category}/{query_id} | Params: {params}")
            logger.warning(f"Integrity Error [do_execute]: {str(e)}")
            # raise
            return {
                "success": False,
                "data": 0,
                "error": {
                    "code": getattr(error_obj, 'code', 'DPY-ERROR'),
                    "message": error_obj.message,
                    "detail": f"Integrity Error: {str(e)}"
                }
            }
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            logger.error(f"Failed API: ~/{category}/{query_id} | Params: {params}")
            logger.error(f"Execution Error [do_execute]: {error_obj.message}")
            # raise
            return {
                "success": False,
                "data": 0,
                "error": {
                    "code": getattr(error_obj, 'code', 'DPY-ERROR'),
                    "message": error_obj.message,
                    "detail": "SQL 바인드 변수와 파라미터가 일치하지 않습니다." if "DPY-4008" in error_obj.message else None
                }
            }