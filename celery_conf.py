from datetime import timedelta
from celery import Celery

app = Celery('tasks')
app.conf.update(
    BROKER_URL='redis://localhost',
    CELERY_TASK_SERIALIZER='json',
    CELERY_IMPORTS = ("tasks.message_notify", ),
    CELERY_ACCEPT_CONTENT=['json'],
    CELERYBEAT_SCHEDULE={
        'save_page': {
            'task': 'tasks.message_notify.message_notify',
            'schedule': timedelta(seconds=30),
        }
    }
)
