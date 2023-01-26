import time

from celery import Celery

from config import CELERY_BROKER_URL, CELERY_BACKEND_URL

app = Celery(__name__)
app.conf.broker_url = CELERY_BROKER_URL
app.conf.result_backend = CELERY_BACKEND_URL


@app.task(name="create_task")
def create_task():
    time.sleep(10)
    return True
