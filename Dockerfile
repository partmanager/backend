FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

RUN mkdir /var/log/shelftracker

RUN apt update && apt install -y rabbitmq-server
