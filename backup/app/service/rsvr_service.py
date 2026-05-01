from backup.app.lib.query_map import get_query
from backup.app.lib.repo import execute, select_one, select_all

# def create_user(user_id: str, user_name: str):
#     sql = get_query("user.create")
#     execute(sql, {"user_id": user_id, "user_name": user_name})
#     return {"result": "ok"}

# def get_user(user_id: str):
#     sql = get_query("user.get_by_id")
#     return select_one(sql, {"user_id": user_id})

def list_equip_rsvr():
    sql = get_query("user.list")
    return select_all(sql)
