FROM python:3.10.8-alpine

EXPOSE 8000

RUN mkdir /instashare && \
    apk upgrade --update

COPY . /instashare
WORKDIR /instashare

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]

CMD ["--workers=4", "app:my_app"]