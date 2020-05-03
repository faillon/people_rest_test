FROM python:3.7-alpine3.9
RUN apk update \
    && apk add --update build-base git make \
    && pip install gunicorn \
    && pip install flask \
    && pip install connexion[swagger-ui] \
    && pip install flask-cors \
    && pip install pymongo \
    && pip install dnspython \
    && pip install pytest


WORKDIR /app
COPY . /app


ENTRYPOINT ["gunicorn", "-w 4", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "server:app"]

