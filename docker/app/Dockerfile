FROM python:3.8.1-alpine

ENV PYTHONUNBUFFERED 1
ENV LANG en_US.utf8

RUN apk upgrade -U
RUN apk add build-base make gcc openssl-dev postgresql-dev
RUN pip3 install --no-cache-dir --upgrade pip
RUN find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY . /app
COPY ./requirements/ /requirements/
COPY ./docker/app/scripts/start-dev.sh /start-dev.sh
COPY ./docker/app/scripts/gunicorn.sh /gunicorn.sh

RUN pip3 install -r /requirements/base.txt

RUN sed -i 's/\r//' /start-dev.sh   && \
    chmod +x /start-dev.sh   && \
    sed -i 's/\r//' /gunicorn.sh   && \
    chmod +x /gunicorn.sh

WORKDIR /app

RUN adduser -D -H -s /bin/bash newuser   && \
    mkdir -p /app/staticfiles   && \
    chown -R newuser /app/staticfiles && \
    mkdir -p /app/media   && \
    chown -R newuser /app/media

USER newuser
