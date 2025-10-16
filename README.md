RSS Digest — Django + Celery

A small Django application that allows an admin to manage RSS news sources, periodically fetch articles using Celery, and manually curate article digests for internal use.

Features

Models:
NewsSource, Article, Digest, DigestArticle (many-to-many through model).

Admin Interface:
Add news sources, view fetched articles, and manually create digests with inline article selection.

Article Fetching:

Manual: via management command python manage.py fetch_articles

Automatic: via Celery periodic tasks (Celery Beat).

Duplicate Prevention:
Unique database constraint on (source, link).

Time Zone:
Europe/Bratislava, USE_TZ=True


Tech Stack

Python 3.11+ (works with 3.13)

Django 5.x

Celery 5.x

Redis (as broker and result backend)

feedparser + requests (RSS fetching and parsing)


Quick Start (Local, without Docker)

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
# http://127.0.0.1:8000/        → public article list
# http://127.0.0.1:8000/admin/ → Django admin

1. Add RSS Sources
Go to /admin, open News Sources, and add one or more feeds.
Make sure they are marked as active=True.

Example RSS feeds:

https://feeds.bbci.co.uk/news/world/rss.xml

https://hnrss.org/frontpage

https://feeds.reuters.com/reuters/topNews


2. Manually Fetch Articles

python manage.py fetch_articles

Background Processing (Celery)
Start Redis Broker

Option 1: Docker

docker run -d --name redis -p 6379:6379 redis:7-alpine

Option 2: macOS / Homebrew

brew install redis
brew services start redis

Make sure these lines exist in config/settings.py or your .env:

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

Run Celery Worker

celery -A config worker -l info

Environment Variables (.env)

Example:

DJANGO_DEBUG=1
DJANGO_SECRET_KEY=dev-secret-key-change-me
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
CELERY_BEAT_SCHEDULE_MINUTES=15
TIME_ZONE=Europe/Bratislava
TIME_INTERVAL=15


Database Structure

NewsSource(name, rss_url, active)

Article(source→NewsSource, title, link, published, summary)

Unique constraint: (source, link)

Digest(name, created_at)

DigestArticle(digest→Digest, article→Article)

Unique constraint: (digest, article)


Admin Workflow

Add one or more RSS sources and activate them.

Run the fetch command or wait for Celery to process them.

Check Articles in the admin panel.

Create a Digest, and use the inline relation to attach selected articles.

Example Fixture (Optional)

news/fixtures/sources.json

[
  {"model": "news.newssource", "pk": 1, "fields": {"name": "BBC World", "rss_url": "https://feeds.bbci.co.uk/news/world/rss.xml", "active": true}},
  {"model": "news.newssource", "pk": 2, "fields": {"name": "Hacker News", "rss_url": "https://hnrss.org/frontpage", "active": true}}
]

Load it:
python manage.py loaddata news/fixtures/sources.json

License

MIT (or specify your own).

Author

Alexander Kiselev
Email: rednaxela1813@gmail.com

Based in Slovakia 🇸🇰
Focus: Django, Vue, SaaS, and automation tools.

