FROM python:3.12-slim

RUN mkdir /app

COPY requirements.lock /app/requirements.lock
RUN sed '/-e/d' /app/requirements.lock > /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

ENV PORT=5000

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
