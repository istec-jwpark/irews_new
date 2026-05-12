
from fastapi import Request, APIRouter, Depends
import json
from core.base_service import Service
from loguru import logger

router = APIRouter(prefix="/geojson", tags=["map_api"])

#GeoJson Site - https://github.com/swcho/korea-maps/tree/main/json

@router.get("/map",
    summary="지도의 영역 표시를 위한 GeoJson",
    description="Example: /category/key?site_sq=1&user_id=a"
)
def geo_json():
    '''접속자의 사이트에 해당하는 GeoJson 정보 가져오기
     Example: /geojson/{user_id}'''
    logger.info(f"###### /geojson (테스트용 서율 경계 데이터) ######")
    with open("./resource/geo_json/korea.json", "r") as f:
        geo_json = json.load(f)
    for info in geo_json['features']:
        logger.info(info['properties'])
    return {
        "type":"FeatureCollection",
        "features":[geo_json['features'][0]]
        }
    # return geo_json['features'][0]
