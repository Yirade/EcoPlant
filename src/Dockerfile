# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder

WORKDIR /app

COPY src/requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev cargo

RUN pip3 install -r requirements.txt --no-cache-dir

COPY src/ .

EXPOSE 8000

WORKDIR /app/EcoPlant/src

ENTRYPOINT ["python3"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]