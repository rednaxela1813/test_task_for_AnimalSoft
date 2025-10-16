#!/usr/bin/env bash

set -e

export DJANGO_SETTINGS_MODULE=config.settings

echo "Waiting for Postgres... at: ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
until nc -z ${POSTGRES_HOST:-db} ${POSTGRES_PORT:-5432}; do
  sleep 0.5
done


python manage.py migrate --noinput
 if [ "${DJANGO_CREATE_SUPERUSER:-1}" = "1" ]; then
  python - <<'PY'
import os
from django.contrib.auth import get_user_model
import django
django.setup()
User = get_user_model()
u = os.getenv("DJANGO_SUPERUSER_USERNAME","admin")
e = os.getenv("DJANGO_SUPERUSER_EMAIL","admin@example.com")
p = os.getenv("DJANGO_SUPERUSER_PASSWORD","adminpass")
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(username=u, email=e, password=p)
    print(f"Superuser created: {u}")
else:
    print(f"Superuser exists: {u}")
PY
fi


exec "$@"