FROM python:3.9.18-alpine3.18

WORKDIR /www/var

COPY requirements.txt .

RUN apk add python3-dev musl-dev postgresql-dev

ARG DATABASE_URL
ARG FLASK_ENV
ARG SCHEMA
ARG SECRET_KEY
ENV VIRTUAL_ENV=/usr/local

RUN pip install uv

RUN uv venv
RUN uv pip install -r requirements.txt
RUN uv pip install psycopg2

COPY . .

RUN source .venv/bin/activate

RUN flask db upgrade
RUN flask seed all

CMD gunicorn --worker-class eventlet -w 1 app:app
