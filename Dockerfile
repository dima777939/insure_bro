FROM python:3.9-alpine
WORKDIR /usr/src/insure_bro
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
