# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN apt-get install curl
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash
RUN apt-get install -y nodejs
RUN npm install -g npm@10.8.0