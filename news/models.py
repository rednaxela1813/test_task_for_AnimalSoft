from django.db import models
from django.utils import timezone
import uuid


class NewsSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    rss_url = models.URLField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    
class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500)
    link = models.URLField()
    published = models.DateTimeField(default=timezone.now)
    summary = models.TextField(blank=True)
    
    
    
    
    class Meta:
        ordering = ['-published']
        constraints = [ 
            models.UniqueConstraint(fields=['source', 'link'], name='uniq_article_source_link')
        ]

    def __str__(self):
        return r"{self.title} ({self.source.name})"

class Digest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    articles = models.ManyToManyField(Article, related_name='digests', blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name
    

class DigestArticle(models.Model):
    digest = models.ForeignKey(Digest, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('digest', 'article')
        verbose_name = 'Digest Article'
        verbose_name_plural = 'Digest Articles'
        
        
    def __str__(self):
        return f"{self.digest} -> {self.article}"