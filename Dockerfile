# FROM python:3.8-slim-buster
FROM gcr.io/google-appengine/python

RUN virtualenv /env -p python3.7
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
# ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get update -y \
&& apt-get install -y gcc libpq-dev libsdl2-dev openssl musl-dev postgresql python3-dev build-essential python3-pip python3-numpy libffi-dev \
&& pip install psycopg2 \
&& pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r /requirements.txt \
&& rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app