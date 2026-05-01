
from fastapi import APIRouter, Depends
from loguru import logger
from core.base_service import Service
# from util.security import require_auth

router = APIRouter(prefix="/equip", tags=["equip"])

@router.get("/rsvr_list/{site_sq}")
def equip_rsvr_list(site_sq:str):
    '''site_sq를 이용하여 rsvr list를 가져온다.'''
    logger.info("###### /rsvr_list ######")
    logger.info("equip_sq : ",site_sq)
    param = {
        "site_sq":site_sq
    }
    _service = Service()
    return _service.find_list("equip","rsvr_current_list_by_site_sq",param)


# @router.get("/rsvr_list", response_model=List[EquipRsvrResponse])
# def equip_rsvr_list(
#     # Depends를 사용하면 URL 쿼리 파라미터(?equip_sq=101)를 Pydantic 모델로 파싱합니다.
#     params: EquipRsvrRequest = Depends(), 
#     user: dict = Depends(require_auth)
# ):