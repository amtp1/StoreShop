FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY .env .env
RUN pip install -r requirements.txt --no-cache-dir

COPY . .