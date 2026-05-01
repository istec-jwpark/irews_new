import yaml
from pathlib import Path

class QueryLoader:
    _queries = {}

    @classmethod
    def load_queries(cls):
        # queries.yaml 경로 설정
        print("###### load queries ######")
        path = Path(__file__).parent.parent / "resource" / "queries.yaml"
        print(path)
        with open(path, "r", encoding="utf-8") as f:
            cls._queries = yaml.safe_load(f)
        print("###### load queries ######")

    @classmethod
    def get(cls, category: str, key: str) -> str:
        return cls._queries.get(category, {}).get(key)

# 앱 가동 시 호출
QueryLoader.load_queries()