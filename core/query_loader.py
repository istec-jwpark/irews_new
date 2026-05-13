import yaml
from pathlib import Path
from loguru import logger

class QueryLoader:
    _queries = {}

    @classmethod
    def load_queries(cls, query_folder='resource'):
        # querie yaml 파일 경로 설정
        logger.info("###### load queries ######")
        base = Path(__file__).parent.parent / query_folder
        for path in base.glob("*.yaml"):
            logger.info(path)
            with open(path, "r", encoding="utf-8") as f:
                cls._queries[path.stem] = yaml.safe_load(f)
        logger.info(cls._queries)
        logger.info("###### load queries ######")

    @classmethod
    def get_type(cls, category:str, key: str) -> bool:
        _type = cls._queries.get(category, {}).get(key,{}).get('type')
        if not _type:
            _type = "query"
        return _type.strip()

    @classmethod
    def get_query(cls, category: str, key: str) -> str:
        return cls._queries.get(category.strip(), {}).get(key.strip(),{}).get('query')
    
    @classmethod
    def get_def(cls, category:str, key: str) -> bool:
        print(category,key)
        return cls._queries.get(category.strip(), {}).get(key.strip(),{}).get('def')

    @classmethod
    def desc(cls, category: str, key: str) -> str:
        _desc = cls._queries.get(category, {}).get(key,{}).get('desc')
        _desc['type'] = cls.get_type(category,key)
        return _desc
    
    @classmethod
    def list(cls):
        _list = {}
        for category in cls._queries:
            if category != 'auth':
                _category = cls._queries.get(category,{})
                if _category:
                    _list[category] = list(_category.keys())
        return _list