FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY src/ /src/

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "infrastructure/manage.py", "runserver", "0.0.0.0:8000"]