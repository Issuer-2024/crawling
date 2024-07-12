import logging
from datetime import datetime


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )
    # 현재 시간 가져오기
    now = datetime.now()

    # 특정 파일 로거 설정
    file_handler = logging.FileHandler(f"app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    job_logger = logging.getLogger('job_logger')
    job_logger.setLevel(logging.INFO)
    job_logger.addHandler(file_handler)


# 로깅 설정을 초기화
setup_logging()
