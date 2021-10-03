FROM python:slim
LABEL author="mauro@sdf.org"

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV USER mozio
ENV HOME /app
WORKDIR $HOME

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -qq \
       libpq-dev gcc zlib1g-dev postgresql-client libpq5 \
       git-core build-essential python3-dev gdal-bin gdal-data \
    && pip3 --no-cache-dir install -U pip \
    && pip3 install -r /app/requirements.txt \
    && rm -fr /app/.cache \
    && groupadd -g $GID $USER \
    && useradd -u $UID -g $USER -s /bin/sh $USER

COPY . /app

EXPOSE 8000
USER $USER
