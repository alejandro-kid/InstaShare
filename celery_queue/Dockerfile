FROM python:3.10.8-slim

RUN apt update
RUN apt upgrade -y

ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

CMD ["celery", "-A tasks", "worker", "-l info", "-E"]
