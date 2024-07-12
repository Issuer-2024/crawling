import datetime
import logging

import pika
import json
import os

from src.file_manager import FileManager
from src.news.news_issue_loader import NewsIssueLoader

logger = logging.getLogger(__name__)

file_manger = FileManager()


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
            delivery_mode=2,  # 메시지를 지속적으로 저장
        ))
    connection.close()


def run_producer():
    main_types = ['News']

    for main_type in main_types:
        logger.info(f"[Start {main_type} Crawling] Starting {main_type} Crawling on {datetime.datetime.now()}")

        if main_type == 'News':
            news_issue_loader = NewsIssueLoader()
            issues = news_issue_loader.crawl_issues()
            logger.info(issues)
            for issue in issues:
                send_task(issue, 'content_queue')
