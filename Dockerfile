FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
MAINTAINER office@tracardi.com

RUN apt-get update
RUN apt-get install -y git

# update pip
RUN /usr/local/bin/python3 -m pip install --upgrade pip

# set the working directory in the container
RUN mkdir app/
WORKDIR /app

## Install dependencies
COPY requirements.txt .
RUN pip install wheel
RUN pip --default-timeout=240 install -r requirements.txt

## Copy application
COPY app app/

ENV VARIABLE_NAME="application"
