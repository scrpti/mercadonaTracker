FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY docker/crontab /etc/cron.d/mercadona-cron
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod 0644 /etc/cron.d/mercadona-cron && \
    crontab /etc/cron.d/mercadona-cron && \
    chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]