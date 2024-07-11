import pika
import json
import os


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
