from django.core.management.base import BaseCommand
from news.models import NewsSource
from news.services import fetch_source_articles


class Command(BaseCommand):
    help  = 'Fetch articles for all active RSS sources'
    
    def handle(self, *args, **options):
        total_created = 0
        
        for src in NewsSource.objects.filter(active=True):
            total_created += fetch_source_articles(src)
        self.stdout.write(self.style.SUCCESS(f"Fetched articles. Total new articles: {total_created}"))