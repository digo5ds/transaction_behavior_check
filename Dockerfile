FROM python:3.12-slim

WORKDIR /transactions

ENV PYTHONPATH=/transactions

COPY requirements.txt .

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic

RUN rm requirements.txt

COPY app/ app/

COPY wait-for-it.sh .

COPY entrypoint.sh .

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]


CMD ["python", "app/api.py"]
