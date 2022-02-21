import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insure_bro.settings")
app = Celery("insure_bro")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
