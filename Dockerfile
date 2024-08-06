FROM python:3.12-slim

LABEL org.opencontainers.image.source=https://github.com/thirdversion/mock-oauth2-service
LABEL org.opencontainers.image.description="Mock OAuth2 Server"
LABEL org.opencontainers.image.licenses=MIT

RUN mkdir /app

COPY requirements.lock /app/requirements.lock
RUN sed '/-e/d' /app/requirements.lock > /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

ENV PORT=5000

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
