import schedule
import time
from src.parallel_processing import run_producer
from src.parallel_processing import run_worker
import logging
from datetime import datetime


logger = logging.getLogger(__name__)
job_logger = logging.getLogger('job_logger')


def job():
    start_time = datetime.now()
    job_logger.info(f"Job started at {start_time}")
    try:
        run_producer()
    except Exception as e:
        logger.error(f"Error occurred during job execution: {e}")
    end_time = datetime.now()
    job_logger.info(f"Job finished at {end_time}")
    job_logger.info(f"Job duration: {end_time - start_time}")


# 정각마다 작업을 실행하도록 스케줄 설정

if __name__ == '__main__':
    logger.info("running")
    schedule.every().hour.at(":00").do(job)
    run_producer()
    run_worker(3)
    while True:
        schedule.run_pending()
        time.sleep(1)


