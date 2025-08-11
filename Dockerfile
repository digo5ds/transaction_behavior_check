FROM python:3.12-slim

WORKDIR /transactions

ENV PYTHONPATH=/transactions

COPY requirements.txt .

RUN apt-get update && apt-get install -y postgresql-client dos2unix && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .

COPY alembic ./alembic

RUN rm requirements.txt

COPY app/ app/

COPY entrypoint.sh .

RUN dos2unix entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]


CMD ["python", "app/api.py"]
