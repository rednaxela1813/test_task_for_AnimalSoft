from django.contrib import admin
from .models import NewsSource, Article, Digest, DigestArticle



@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_url', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('name', 'rss_url')
    
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published', 'link')
    list_filter = ('source',)
    search_fields = ('title', 'summary', 'link')
    date_hierarchy = 'published'
    
    
class DigestArticleInline(admin.TabularInline):
    model = DigestArticle
    extra = 1
    autocomplete_fields = ('article',)
    
    
@admin.register(Digest)
class DigestAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    #date_hierarchy = 'created_at'
    inlines = [DigestArticleInline]
    search_fields = ('name',)
    
    
@admin.register(DigestArticle)
class DigestArticleAdmin(admin.ModelAdmin):
    list_display = ('digest', 'article')
    search_fields = ('digest__name', 'article__title')
    autocomplete_fields = ('digest', 'article')