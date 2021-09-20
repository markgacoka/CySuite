FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update --no-cache \
&& apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add curl-dev gcc libc-dev libffi-dev libxml2-dev linux-headers postgresql \
    postgresql-dev python3-dev jpeg-dev libjpeg zlib zlib-dev \
&& pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r /requirements.txt \
&& pip install Pillow \
&& apk del --no-cache --purge build-deps
RUN apk add postgresql-libs libpq --no-cache
WORKDIR /usr/src/app

RUN adduser -D user
USER user