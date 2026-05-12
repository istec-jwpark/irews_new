import os
import inspect
from importlib import util as importlib_util
from typing import get_type_hints
from pathlib import Path
from loguru import logger

class FilterLoader:
    # 로드된 함수들을 담을 클래스 변수 (공유 저장소)
    _filters = {}

    @classmethod
    def load_filter(cls,filter_folder='filter'):
        """특정 폴더의 모든 .py 파일에서 함수를 로드하여 클래스 변수에 저장합니다."""
        logger.info("###### load service ######")
        folder_path = Path(__file__).parent.parent / filter_folder
        if not os.path.exists(folder_path):
            print(f"Error: 경로 '{folder_path}'를 찾을 수 없습니다.")
            return
        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and filename != "__init__.py":
                category = filename[:-3]
                file_path = os.path.join(folder_path, filename)
                cls._filters[category] = {}
                try:
                    # 모듈 로드 설정
                    spec = importlib_util.spec_from_file_location(category, file_path)
                    module = importlib_util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 해당 모듈 내의 함수들만 추출
                    for func_name, func_obj in inspect.getmembers(module, inspect.isfunction):
                        # 자신이 직접 정의한 함수인지 체크 (외부 import 함수 제외)
                        if func_obj.__module__ == category:
                            # 함수 시그니처 및 타입 힌트 확인
                            sig = inspect.signature(func_obj)
                            hints = get_type_hints(func_obj)
                            # 파라미터 타입 추출 (타입 힌트가 없는 경우 제외)
                            params = list(sig.parameters.values())
                            return_type = hints.get('return')
                            # 검증 조건 (파라미터 개수, 타입, 리턴 타입 일치 여부)
                            if len(params) == 2 and \
                                hints.get(params[0].name) == str and\
                                hints.get(params[1].name) == dict and\
                                return_type == (str, dict):
                                cls._filters[category][func_name] = func_obj
                            else:
                                logger.info(f"❌ 제외됨: {func_name} (타입 불일치)")
                except Exception as e:
                    logger.info(f"Module '{filename}' 로드 실패: {e}")
        logger.info(cls._filters)
        logger.info("###### load service ######")

    @classmethod
    def run(cls, category, func_name, *args, **kwargs):
        """저장된 함수를 이름으로 찾아 실행합니다."""
        func = cls._filters.get(category,{}).get(func_name)
        if func:
            return func(*args, **kwargs)
        else:
            print(f"Error: 함수 '{func_name}'가 로드되지 않았습니다.")
            return None

    @classmethod
    def get(cls, category: str, key: str) -> str:
        return cls._filters.get(category, {}).get(key,{})

    @classmethod
    def list(cls):
        _list = {}
        for category in cls._filters:
            if category != 'auth':
                _list[category] = list(cls._filters.get(category,{}).keys())
        return _list