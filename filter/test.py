def test(query:str, param:dict) -> (str, dict):
    # siteSq(str), activeCode(str)
    print("test filter")
    _query = query;
    _param = param;
    _siteSq = _param.get('siteSq')
    _activeCode = _param.get('activeCode')
    if _siteSq:
        _query = _query + "\n and site_sq = :siteSq"
    if _activeCode:
        _query = _query + "\n and active_code = :activeCode"
    return (_query, _param)