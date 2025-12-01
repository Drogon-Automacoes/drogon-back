FROM python:3.11-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app
COPY ./scripts ./scripts

CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"

