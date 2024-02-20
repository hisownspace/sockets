FROM python:3.9-alpine

WORKDIR /www/var

COPY requirements.txt .

RUN apk add python3-dev musl-dev postgresql-dev

ARG SECRET_KEY
ARG FLASK_ENV
ARG DATABASE_URL
ARG VIRTUAL_ENV

RUN pip install uv

RUN uv venv
RUN uv pip install -r requirements.txt
RUN uv pip install psycopg2

COPY . .

RUN flask db upgrade
RUN flask seed all

CMD gunicorn --worker-class eventlet -w 1 app:app
