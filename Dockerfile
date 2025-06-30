FROM python:3.12

ENV DAGSTER_HOME=/opt/dagster/home/
ENV PYTHONPATH=$DAGSTER_HOME/app

RUN mkdir -p $DAGSTER_HOME && \
    mkdir -p $DAGSTER_HOME/app && \
    mkdir -p $DAGSTER_HOME/artifacts

WORKDIR $DAGSTER_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dagster.yaml workspace.yaml ./
COPY app/ app/
