from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simple_Stay_backend.settings')

app = Celery('Simple_Stay_backend')
app.conf.enable_utc = False


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    task_concurrency=4,
    timezone='Asia/Kolkata'
)


app.conf.beat_schedule = {
    'check-package-expiration': {
        'task': 'premium.tasks.check_package_expiration',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
