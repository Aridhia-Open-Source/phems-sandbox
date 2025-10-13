FROM r-base:4.5.1

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*


# Install Dagster Pipes in Python
RUN pip3 install --no-cache-dir dagster dagster-pipes

RUN R -e "install.packages('jsonlite', repos='https://cloud.r-project.org')"

WORKDIR /usr/local/src/scripts

ENTRYPOINT ["python3", "entrypoint.py"]
