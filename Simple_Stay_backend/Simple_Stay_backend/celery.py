# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from django.conf import settings

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simple_Stay_backend.settings')

# # create a Celery instance and configure it.
# app = Celery('Simple_Stay_backend')

# #Disabling default timezone as UTC
# app.conf.enable_utc = False

# app.conf.update(timezone = 'Asia/Kolkata')

# app.config_from_object(settings, namespace='CELERY')

# # app.conf.beat_schedule = {

# # }


# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")


from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simple_Stay_backend.settings')

app = Celery('Simple_Stay_backend')
# app.conf.enable_utc = False

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    task_concurrency=4,  # Set the concurrency to 4, for example
    # Other Celery settings...
)

if __name__ == '__main__':
    app.start()
    

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

