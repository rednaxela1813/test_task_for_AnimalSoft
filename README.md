# 📰 RSS Digest — Django + Celery + Redis + PostgreSQL

RSS Digest is a minimal Django-based backend application that periodically fetches and stores news articles from multiple RSS sources.  
It demonstrates background task processing with Celery and Redis, containerized deployment using Docker Compose, and robust error handling.

---

## 🧩 Features

- Django 5 + PostgreSQL (persistent storage)
- Celery workers + Celery Beat (scheduled RSS updates)
- Redis (message broker + result backend)
- Automatic periodic fetching every 15 minutes
- Graceful error handling for broken or unreachable RSS feeds
- Easy management via Django Admin (`/admin`)
- Fully containerized with Docker Compose

---

## 🏗️ Project Structure


---

## ⚙️ Environment Variables (`.env`)

Example:

```env
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=*

POSTGRES_DB=rssdigest
POSTGRES_USER=rssuser
POSTGRES_PASSWORD=rsspass
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

docker compose up --build

This launches:

Service	Description
web	Django app (runserver)
worker	Celery worker processing tasks
beat	Celery Beat scheduler (runs every 15 min)
db	PostgreSQL
redis	Redis (broker + result backend)

Then visit:
👉 http://localhost:8000/admin

and log in using credentials from .env

How It Works

Add RSS sources in Django Admin → News Sources
e.g.

https://feeds.bbci.co.uk/news/world/rss.xml

https://hnrss.org/frontpage

https://www.theguardian.com/world/rss

Celery Beat triggers fetch_all_sources every 15 minutes.
Each source is fetched by the worker, parsed via feedparser, and stored in the database.

The system gracefully ignores:

Broken links

Fetch all active sources manually:

docker compose exec web python manage.py fetch_articles


🧑‍💻 Author

Alexander Kiselev
📍 Slovakia
📧 rednaxela1813@gmail.com

🌐 https://deilmann.sk

🧾 License

MIT — feel free to reuse this template for educational or demonstration purposes.

