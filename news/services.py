from django.utils import timezone
from .models import NewsSource, Article
import feedparser
from datetime import datetime
import time


def _entry_published_dt(entry) -> datetime:
    tm = getattr(entry, "published_parser", None) or entry.get("published_parsed", None)
    if tm:
        try:
            ts = time.mktime(tm)
            return datetime.fromtimestamp(ts, tz=timezone.get_current_timezone())
        except Exception:
            pass
    return timezone.now()


def fetch_source_articles(source: NewsSource) -> int:
    created_count = 0
    parsed = feedparser.parse(source.rss_url)
    
    
    for e in parsed.entries:
        link = e.get("link") or ""
        if not link:
            continue
        published = _entry_published_dt(e)
        title = e.get("title", "(No title)")
        summary = e.get("summary", "")  
        
        _, created = Article.objects.get_or_create(
            source=source,
            link=link,
            defaults={
                "title": title[:500],
                "published": published,
                "summary": summary,
            }
        )
        if created:
            created_count += 1
    return created_count
    