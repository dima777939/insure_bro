FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y postgresql-contrib
WORKDIR /usr/src/insure_bro
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
