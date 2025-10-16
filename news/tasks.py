from celery import shared_task
from .models import NewsSource
from .services import fetch_source_articles


@shared_task
def fetch_source(source_id: int)  -> int:
    try:
        src = NewsSource.objects.get(id=source_id, active=True)
    except NewsSource.DoesNotExist:
        return 0
    return fetch_source_articles(src)


@shared_task
def fetch_all_sources() -> int:
    total = 0
    for src in NewsSource.objects.filter(active=True):
        total += fetch_source_articles(src)
    return total