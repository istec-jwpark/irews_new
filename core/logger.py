from fastapi import Request
from loguru import logger
import sys, time
# 1. Loguru 설정
# 기본 콘솔 핸들러 제거
logger.remove()
# 콘솔 출력 설정
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}")
# 파일 출력 설정: 매일(daily) 생성, 7일간 보관
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log", 
    rotation="00:00",    # 매일 자정에 새로운 파일 생성
    retention="7 days",   # 7일이 지난 로그는 자동 삭제
    compression="zip",    # (옵션) 오래된 로그는 압축해서 저장
    level="INFO"
)

async def log_middleware(request: Request, call_next):
    start_time = time.time()
    # 요청 정보 추출
    method = request.method
    url = request.url.path
    client_ip = request.client.host
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        # 로그 기록
        logger.info(
            f"IP: {client_ip} | Method: {method} | URL: {url} | "
            f"Status: {response.status_code} | Time: {process_time:.2f}ms"
        )
        return response
    except Exception as e:
        # 에러 발생 시 상세 정보 기록
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"IP: {client_ip} | Method: {method} | URL: {url} | "
            f"Error: {str(e)} | Time: {process_time:.2f}ms"
        )
        raise e