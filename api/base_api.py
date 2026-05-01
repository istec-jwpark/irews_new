from fastapi import Request, APIRouter, Depends
from loguru import logger
from core.base_service import Service
from core.query_loader import QueryLoader
# from util.security import require_auth

router = APIRouter(prefix="/api", tags=["base_api"])

@router.get("/list", summary="api map list")
def api_map_list():
    return QueryLoader.list()

@router.get("/info/{category}/{key}", summary="api key infomation")
def api_key_info(category:str, key:str):
    '''category(쿼리맵 파일명), key(쿼리 ID)를 이용하여 해당 key의 정보 제공
     Example: /api/info/category/key'''
    return QueryLoader.desc(category,key)


@router.get("/{category}/{key}",
    summary="api category의 key에 대한 결과 조회",
    description="Example: /category/key?site_sq=1&user_id=a"
)
def select(category:str, key:str, request:Request):
    '''category(쿼리맵 파일명), key(쿼리 ID), 파라미터를 이용하여 DB 조회를 통해 결과를 읽어온다
     Example: /api/category/key?site_sq=1&user_id=a'''
    logger.info(f"###### /api/{category}/{key} ######")
    param = dict(request.query_params)
    # print(param)
    logger.info(param)
    _service = Service()
    return _service.find_list(category,key,param)
