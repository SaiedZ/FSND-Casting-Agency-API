# set the Base Image from which your image will be built on
FROM python:3.10-alpine
LABEL maintainer="Saied"

# set environment variables
# Python won’t try to write .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD gunicorn  --bind 0.0.0.0:$PORT flaskr.wsgi:app