from loguru import logger

def test(params:dict) -> (str,dict):
    print("test service")
    _params = params.copy()
    _siteSq = ""
    _activeCode = ""
    logger.info(_params)
    if _params.get("siteSq"):
        _siteSq = "AND SITE_SQ = :siteSq"
    if _params.get("activeCode"):
        _activeCode = "AND ACTIVE_CODE = :activeCode"
    _query = f"""SELECT * FROM TB_EQUIP_INFO_BASE E JOIN TB_M1_INFO_POINT_BASE P ON E.POINT_SQ = P.SITE_SQ
    WHERE 1=1 {_siteSq} {_activeCode}"""
    logger.info(_query)
    return (_query, _params)