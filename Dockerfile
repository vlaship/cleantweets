FROM python:3.5.2-alpine

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r /app/requirements.txt
