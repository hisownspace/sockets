FROM python:3.9-alpine

WORKDIR /www/var

COPY requirements.txt .

RUN apk add python3-dev musl-dev postgresql-dev

ENV SECRET_KEY=password
ENV FLASK_ENV=development
ENV DATABASE_URL=sqlite:///dev.db

ENV VIRTUAL_ENV=/usr/local

RUN pip install uv

RUN uv venv
RUN uv pip install -r requirements.txt
RUN uv pip install psycopg2

COPY . .

RUN flask db upgrade
RUN flask seed all

CMD gunicorn --worker-class eventlet -w 1 app:app -b 0.0.0.0:5000
