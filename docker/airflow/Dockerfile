# Base Image
FROM spark-base:latest
LABEL maintainer="GiaThe"

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=2.8.0
ARG AIRFLOW_HOME=/usr/local/airflow
ARG PYTHON_VERSION=3.9

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install dependencies and tools
RUN apt-get update -y && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    python3-dev \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev \
    libpq-dev \
    freetds-bin \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    vim \
    netcat \
    && apt-get autoremove -yqq --purge && apt-get clean

# Use the correct constraints file for Python 3.9
COPY ./requirements-python3.9.txt /requirements-python3.9.txt
# Install Airflow using the correct constraint file and add Spark provider
RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh,docker,hdfs,redis,slack,webhdfs,spark]==${AIRFLOW_VERSION} \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
    --root-user-action=ignore

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./start-airflow.sh ./start-airflow.sh

# Set the entrypoint.sh file to be executable
RUN chmod +x ./start-airflow.sh

# Set the username to use
USER airflow

# Create the folder dags inside $AIRFLOW_HOME
RUN mkdir -p ${AIRFLOW_HOME}/dags

# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080

# Execute start-airflow.sh
CMD [ "./start-airflow.sh" ]
