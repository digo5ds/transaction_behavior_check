FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

COPY app .

RUN python manage.py 

EXPOSE 5001

CMD ["python", "api.py"]