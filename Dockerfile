FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./prestart.sh /app/prestart.sh

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

