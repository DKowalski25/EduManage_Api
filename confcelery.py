from celery import Celery
from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
app = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['app.tasks.email_tasks']
)

app.conf.update(
    task_routes={
        'app.tasks.email_tasks.send_email_task': {'queue': 'email_queue'}
    }
)