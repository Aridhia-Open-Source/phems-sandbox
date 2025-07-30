FROM python:3.12-slim

ENV DAGSTER_HOME=/opt/dagster/home/
ENV PYTHONPATH=$DAGSTER_HOME/app
WORKDIR $DAGSTER_HOME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY workspace.yaml .
COPY app app
