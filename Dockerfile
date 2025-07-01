FROM python:3.12

ENV DAGSTER_HOME=/opt/dagster/home/
ENV PYTHONPATH=$DAGSTER_HOME/app
WORKDIR $DAGSTER_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dagster.yaml workspace.yaml celery.yaml ./
COPY app/ app/
