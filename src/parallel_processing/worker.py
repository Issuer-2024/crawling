import json

from src.file_manager import FileManager
import logging

from src.news import NewsContentCrawler

logger = logging.getLogger(__name__)

file_manager = FileManager()

job_logger = logging.getLogger('job_logger')


def process_content_task(body):
    task = json.loads(body.decode('utf-8'))
    logger.info(task)
    try:
        # 메시지를 UTF-8로 디코딩하여 JSON으로 로드
        news_content_crawler = NewsContentCrawler()
        data = news_content_crawler.crawl_content(task['URL'])
        file_manager.save(task | data, 'ISSUE', 'NEWS')
        comments_url = news_content_crawler.convert_comments_url(task['URL'])
        send_task({'status': 'completed', 'task': task}, 'completed_tasks_queue')
        send_task({'comments_url': comments_url}, 'comments_queue')
        job_logger.info(f"[Crawling Success] task: {task}")
    except Exception as e:
        logger.error(f"[Error Processing Task]: {task}")
        # 실패한 작업을 다시 큐에 보내기
        retry_task = {'URL': task['URL'], 'retry_count': task.get('retry_count', 0) + 1}
        if retry_task['retry_count'] <= 2:  # 재시도 횟수 제한 설정
            send_task(retry_task, 'content_queue')
        else:
            send_task(retry_task, 'failed_tasks_queue')  # 일정 횟수 이상 실패한 작업은 별도 큐에 저장
            job_logger.info(f"[!!Crawling Failed!!] task: {task}")

def process_comments_task(body):
    task = json.loads(body.decode('utf-8'))
    try:
        news_comments_crawler = NewsCommentsCrawler()
        data = news_comments_crawler.crawl_comments(task['comments_url'])
        file_manager.save(data, 'ISSUE_COMMENTS', 'NEWS')
        send_task({'status': 'completed', 'task': task}, 'completed_tasks_queue')
        job_logger.info(f"[Crawling Success] task: {task}")
    except Exception as e:
        logger.error(f"Error Processing Task: {task}")
        retry_task = {'comments_url': task['comments_url'], 'retry_count': task.get('retry_count', 0) + 1}
        if retry_task['retry_count'] <= 2:
            send_task(retry_task, 'comments_queue')
        else:
            send_task(retry_task, 'failed_tasks_queue')
        job_logger.info(f"[!!Crawling Failed!!] task: {task}")
