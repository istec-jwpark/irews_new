import yaml
from pathlib import Path
from loguru import logger

class QueryLoader:
    _queries = {}

    @classmethod
    def load_queries(cls):
        # querie yaml 파일 경로 설정
        logger.info("###### load queries ######")
        base = Path(__file__).parent.parent / "resource"
        for path in base.glob("*.yaml"):
            logger.info(path)
            with open(path, "r", encoding="utf-8") as f:
                cls._queries[path.stem] = yaml.safe_load(f)
        logger.info(cls._queries)
        logger.info("###### load queries ######")

    @classmethod
    def get(cls, category: str, key: str) -> str:
        return cls._queries.get(category, {}).get(key,{}).get('query')

    @classmethod
    def desc(cls, category: str, key: str) -> str:
        return cls._queries.get(category, {}).get(key,{}).get('desc')
    
    @classmethod
    def list(cls):
        query_list = {}
        for category in cls._queries:
            query_list[category] = list(cls._queries[category].keys())
        return query_list
# 앱 가동 시 호출
QueryLoader.load_queries()