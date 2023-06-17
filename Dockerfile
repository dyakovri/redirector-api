FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV APP_NAME=redirector
ENV APP_MODULE=${APP_NAME}.main:app

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations
COPY ./${APP_NAME} /app/${APP_NAME}
