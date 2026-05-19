import yaml
import os
from pathlib import Path
from loguru import logger
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

class QueryReloaderHandler(FileSystemEventHandler):
    """파일 변경 이벤트를 처리하는 핸들러"""
    def __init__(self, loader_cls, folder_path):
        self.loader_cls = loader_cls
        self.folder_path = folder_path

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".yaml"):
            logger.info(f"🔄 Query file changed: {event.src_path}. Reloading...")
            self.loader_cls.load_queries(self.folder_path)

class QueryLoader:
    _queries = {}
    _observer = None

    @classmethod
    def load_queries(cls, query_folder='resource'):
        """YAML 파일을 읽어 메모리에 로드합니다."""
        logger.info(f"###### Loading queries from '{query_folder}' ######")
        # 프로젝트 루트 기준으로 경로 설정
        base = Path(__file__).parent.parent / query_folder
        
        if not base.exists():
            logger.error(f"Directory not found: {base}")
            return

        new_queries = {}
        for path in base.glob("*.yaml"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                    if content:
                        new_queries[path.stem] = content
            except Exception as e:
                logger.error(f"Failed to load {path.name}: {e}")
        
        cls._queries = new_queries
        logger.info(f"✅ Loaded categories: {list(cls._queries.keys())}")

        # 최초 로드 시 감시자(Observer) 시작
        if cls._observer is None:
            cls._start_watchdog(query_folder, base)

    @classmethod
    def _start_watchdog(cls, folder_name, folder_path):
        """파일 시스템 변경 감지 시작"""
        event_handler = QueryReloaderHandler(cls, folder_name)
        cls._observer = Observer()
        cls._observer.schedule(event_handler, str(folder_path), recursive=False)
        cls._observer.start()
        logger.info(f"👀 Started watching query folder: {folder_path}")

    @classmethod
    def stop_watchdog(cls):
        """앱 종료 시 감시자 중지"""
        if cls._observer:
            cls._observer.stop()
            cls._observer.join()
            logger.info("🛑 Query watchdog stopped.")

    # --- 기존 메서드 유지 (get_type, get_query, get_def, list 등) ---
    @classmethod
    def get_query(cls, category: str, key: str) -> str:
        return cls._queries.get(category.strip(), {}).get(key.strip(), {}).get('query')

    @classmethod
    def list(cls):
        return {cat: list(cls._queries[cat].keys()) for cat in cls._queries if cat != 'auth'}