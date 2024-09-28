#!/usr/bin/env bash

# Create the user airflow in the HDFS
hdfs dfs -mkdir -p /user/airflow/
hdfs dfs -chmod g+w /user/airflow

# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initialize the metadatabase
airflow db init

# Create Airflow user (if not already created)
airflow users create \
    --username airflow \
    --password airflow \
    --firstname FirstName \
    --lastname LastName \
    --role Admin \
    --email admin@example.com

# Run the scheduler in the background
airflow scheduler &> /dev/null &

# Run the webserver in foreground (so docker logs can capture it)
exec airflow webserver
