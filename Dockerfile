FROM python:3.10.8-slim

EXPOSE 8000

RUN apt update
RUN apt upgrade -y

RUN mkdir /instashare
COPY . /instashare
WORKDIR /instashare

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]

CMD ["--workers=4", "app:instashare"]
