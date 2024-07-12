import os

import pika
import json

from src.file_manager import FileManager
from concurrent.futures import ThreadPoolExecutor
import logging

from src.news import NewsContentCrawler, NewsCommentsCrawler

logger = logging.getLogger(__name__)


def send_task(task, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL'), 5672))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    message = json.dumps(task)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message.encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()


def process_content_task(body):
    task = json.loads(body.decode('utf-8'))
    logger.error(task)
    try:
        # 메시지를 UTF-8로 디코딩하여 JSON으로 로드
        news_content_crawler = NewsContentCrawler()
        data = news_content_crawler.crawl_content(task['URL'])
        file_manager = FileManager()
        file_manager.save(task | data, 'ISSUE', 'NEWS')
        comments_url = news_content_crawler.convert_comments_url(task['URL'])
        send_task({'status': 'completed', 'task': task}, 'completed_tasks_queue')
        send_task({'comments_url': comments_url}, 'comments_queue')
        logger.info(f"[Crawling Success] task: {task}")
    except Exception as e:
        logger.error(f"[Error Processing Task]: {task}")
        # 실패한 작업을 다시 큐에 보내기
        retry_task = {'URL': task['URL'], 'retry_count': task.get('retry_count', 0) + 1}
        if retry_task['retry_count'] <= 2:  # 재시도 횟수 제한 설정
            send_task(retry_task, 'content_queue')
        else:
            send_task(retry_task, 'failed_tasks_queue')  # 일정 횟수 이상 실패한 작업은 별도 큐에 저장
            logger.info(f"[!!Crawling Failed!!] task: {task}")


def process_comments_task(body):
    task = json.loads(body.decode('utf-8'))
    try:
        news_comments_crawler = NewsCommentsCrawler()
        data = news_comments_crawler.crawl_comments(task['comments_url'])
        file_manager = FileManager()
        file_manager.save(data, 'ISSUE_COMMENTS', 'NEWS')
        send_task({'status': 'completed', 'task': task}, 'completed_tasks_queue')
        logger.info(f"[Crawling Success] task: {task}")
    except Exception as e:
        logger.error(f"Error Processing Task: {task}")
        retry_task = {'comments_url': task['comments_url'], 'retry_count': task.get('retry_count', 0) + 1}
        if retry_task['retry_count'] <= 2:
            send_task(retry_task, 'comments_queue')
        else:
            send_task(retry_task, 'failed_tasks_queue')
        logger.info(f"[!!Crawling Failed!!] task: {task}")


def callback(ch, method, properties, body, executor, task_type):
    if task_type == 'content':
        executor.submit(process_content_task, body)
    elif task_type == 'comments':
        executor.submit(process_comments_task, body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_worker(max_workers):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL'), 5672))
    channel = connection.channel()

    channel.queue_declare(queue='content_queue', durable=True)
    channel.queue_declare(queue='comments_queue', durable=True)
    channel.queue_declare(queue='completed_tasks_queue', durable=True)
    channel.queue_declare(queue='failed_tasks_queue', durable=True)

    executor = ThreadPoolExecutor(max_workers=max_workers)  # 스레드 풀 생성, 최대 5개의 스레드

    # 큐에서 메시지 소비를 설정
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='content_queue',
                          on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties,
                                                                                            body, executor, 'content'))
    channel.basic_consume(queue='comments_queue',
                          on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties,
                                                                                            body, executor, 'comments'))

    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
