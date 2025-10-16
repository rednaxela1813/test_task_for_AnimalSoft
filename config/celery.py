import os
from celery import Celery
from datetime import timedelta
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

time_interval = config('TIME_INTERVAL', default=15, cast=int)

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "fetch-rss-every-15-min": {
        "task": "news.tasks.fetch_all_sources",
        "schedule": timedelta(minutes=time_interval),
    }
}