FROM python:3.10

RUN apt-get update && apt-get -y install cron vim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY crontab /etc/cron.d/crontab
COPY requirements.txt requirements.txt

RUN touch /tmp/out.log \
    && pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && crontab /etc/cron.d/crontab

COPY . .
CMD ["cron", "-f"]