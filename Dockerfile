FROM python:3.9.18-alpine3.18

WORKDIR /www/var

COPY requirements.txt .

RUN apk add python3-dev musl-dev postgresql-dev

ARG DATABASE_URL
ARG FLASK_ENV
ARG SCHEMA
ARG SECRET_KEY
# ENV VIRTUAL_ENV=/www/var/venv

# ADD --chmod=755 https://astral.sh/uv/install.sh ./install.sh
# RUN ./install.sh && rm ./install.sh

# ENV PATH="/root/.cargo/bin:$PATH"

# RUN uv venv $VIRTUAL_ENV

# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY . .

RUN flask db upgrade
RUN flask seed all

CMD gunicorn --worker-class eventlet -w 1 app:app
