FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    redis \
    grafana \
    prometheus \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

RUN python manage.py migrate

CMD ["gunicorn", "my_tennis_club.wsgi:application", "--bind", "0.0.0.0:8000"]
