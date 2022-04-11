from celery import Celery

rabbitmq = 'rabbitmq_message_broker'

app = Celery('tasks', broker=rabbitmq)
