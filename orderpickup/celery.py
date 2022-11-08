import os

from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orderpickup.settings")

app = Celery("orderpickup")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'driver.tasks.get_drivers_task',
        'schedule': crontab(minute=30),
    },
}