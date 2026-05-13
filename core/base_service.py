from typing import List, Dict, Any, Optional
from core.database import db_manager
from core.query_loader import QueryLoader
from core.filter_loader import FilterLoader
from core.service_loader import ServiceLoader
from core.query_executor import QueryExecutor
from loguru import logger

class Service:
    def _get_sql(self, category: str, query_id: str) -> str:
        sql = QueryLoader.get_query(category, query_id)
        logger.info(f"****** QUERY Category/ID : {category}/{query_id}")
        logger.info(sql)
        if not sql:
            raise ValueError(f"Query ID '{query_id}' not found in category '{category}'")
        return sql

    def find_one(self, category: str, query_id: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        logger.info(f"****** params : {params}")
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                return QueryExecutor.fetch_one(cursor, self._get_sql(category,query_id), params)

    def find_list(self, category: str, query_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
            1. 타입 체크
            2. query 이면 query 수행처리
            3. def 이면 service 함수 처리 결과(query, params)를 이용 수행 처리
        """
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                _type = QueryLoader.get_type(category, query_id)
                logger.info(f"%%% Check Query Type : {_type}")
                if _type == 'def':
                    ## filter 함수 처리 대상이면 함수 호출하여 처리된 쿼리를 받아
                    _def = QueryLoader.get_def(category, query_id)
                    _service = ServiceLoader.get(_def.strip())
                    logger.info(f"%%% Service function : {_def}/{_service}")
                    if _service:
                        _sql,_params = _service(params)
                        logger.info(f"%%% Filter result : {_sql}, {_params}")
                        return QueryExecutor.fetch_all(cursor, _sql,_params)    
                return QueryExecutor.fetch_all(cursor, self._get_sql(category, query_id), params)

    def do_execute(self, category: str, query_id: str, params: Dict[str, Any] = None) -> int:
        """입력, 수정, 삭제 공통 (affected rows 반환)"""
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                return QueryExecutor.execute(cursor, self._get_sql(category, query_id), params)
