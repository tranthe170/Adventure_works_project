from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 9, 20),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="adventure_works",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    # Task to download the Customer.csv file
    download_customer_data = BashOperator(
        task_id="download_customer_data",
        bash_command="""curl -o /usr/local/airflow/dags/files/Customer.csv https://raw.githubusercontent.com/AhmadSabbirChowdhury/Microsoft-AdventureWorks-Database-Analysis-Visualization-with-PowerBI/refs/heads/main/CSV%20Files/DIM_Customer.csv""",
    )

    # Task to download the Product.csv file
    download_product_data = BashOperator(
        task_id="download_product_data",
        bash_command="""curl -o /usr/local/airflow/dags/files/Product.csv https://raw.githubusercontent.com/AhmadSabbirChowdhury/Microsoft-AdventureWorks-Database-Analysis-Visualization-with-PowerBI/refs/heads/main/CSV%20Files/DIM_Products.csv""",
    )

    # Task to download the Date.csv file
    download_date_data = BashOperator(
        task_id="download_date_data",
        bash_command="""curl -o /usr/local/airflow/dags/files/Date.csv https://raw.githubusercontent.com/AhmadSabbirChowdhury/Microsoft-AdventureWorks-Database-Analysis-Visualization-with-PowerBI/refs/heads/main/CSV%20Files/Dim_Date_Excel.csv""",
    )

    # Task to download the InternetSale.csv file
    download_internet_sale_data = BashOperator(
        task_id="download_internet_sale_data",
        bash_command="""curl -o /usr/local/airflow/dags/files/InternetSale.csv https://raw.githubusercontent.com/AhmadSabbirChowdhury/Microsoft-AdventureWorks-Database-Analysis-Visualization-with-PowerBI/refs/heads/main/CSV%20Files/FactInternetSale.csv""",
    )

    # FileSensors to check if the files are present
    check_customer_file = FileSensor(
        task_id="check_customer_file",
        filepath="/usr/local/airflow/dags/files/Customer.csv",
        poke_interval=5,
        timeout=20,
    )

    check_product_file = FileSensor(
        task_id="check_product_file",
        filepath="/usr/local/airflow/dags/files/Product.csv",
        poke_interval=5,
        timeout=20,
    )

    check_date_file = FileSensor(
        task_id="check_date_file",
        filepath="/usr/local/airflow/dags/files/Date.csv",
        poke_interval=5,
        timeout=20,
    )

    check_internet_sale_file = FileSensor(
        task_id="check_internet_sale_file",
        filepath="/usr/local/airflow/dags/files/InternetSale.csv",
        poke_interval=5,
        timeout=20,
    )

    # Task to upload Customer.csv to HDFS
    save_customer_to_hdfs = BashOperator(
        task_id="save_customer_to_hdfs",
        bash_command="""hdfs dfs -mkdir -p /adventure_works && hdfs dfs -put -f /usr/local/airflow/dags/files/Customer.csv /adventure_works/""",
    )

    # Task to upload Product.csv to HDFS
    save_product_to_hdfs = BashOperator(
        task_id="save_product_to_hdfs",
        bash_command="""hdfs dfs -mkdir -p /adventure_works && hdfs dfs -put -f /usr/local/airflow/dags/files/Product.csv /adventure_works/""",
    )

    # Task to upload Date.csv to HDFS
    save_date_to_hdfs = BashOperator(
        task_id="save_date_to_hdfs",
        bash_command="""hdfs dfs -mkdir -p /adventure_works && hdfs dfs -put -f /usr/local/airflow/dags/files/Date.csv /adventure_works/""",
    )

    # Task to upload InternetSale.csv to HDFS
    save_internet_sale_to_hdfs = BashOperator(
        task_id="save_internet_sale_to_hdfs",
        bash_command="""hdfs dfs -mkdir -p /adventure_works && hdfs dfs -put -f /usr/local/airflow/dags/files/InternetSale.csv /adventure_works/""",
    )

    # Create adventure_works schema
    create_adventure_works_schema = HiveOperator(
        task_id="create_adventure_works_schema",
        hive_cli_conn_id="hive_conn",
        hql="""CREATE SCHEMA IF NOT EXISTS adventure_works;""",
    )

    # Create Customer table
    create_customer_table = HiveOperator(
        task_id="create_customer_table",
        hive_cli_conn_id="hive_conn",
        hql="""CREATE EXTERNAL TABLE IF NOT EXISTS adventure_works.Customer (
                CustomerKey INT,
                `First Name` STRING,
                `Last Name` STRING,
                `Full Name` STRING,
                Gender STRING,
                DateFirstPurchase DATE,
                `Customer City` STRING
            ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;""",
    )

    # Create Product table
    create_product_table = HiveOperator(
        task_id="create_product_table",
        hive_cli_conn_id="hive_conn",
        hql="""CREATE EXTERNAL TABLE IF NOT EXISTS adventure_works.Product (
                ProductKey INT,
                ProductItemCode STRING,
                `Product Name` STRING,
                `Sub Category` STRING,
                `Product Category` STRING,
                `Product Color` STRING,
                `Product Size` STRING,
                `Product Line` STRING,
                `Product Model Name` STRING,
                `Product Description` STRING,
                `Product Status` STRING
            ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;""",
    )

    # Create Date table
    create_date_table = HiveOperator(
        task_id="create_date_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS adventure_works.DateTable (
                DateKey STRING,
                FullDate STRING,
                Day STRING,
                WeekNumber STRING,
                Month STRING,
                MonthShort STRING,
                MonthNumber STRING,
                Quater STRING,
                Year STRING
            ) 
            ROW FORMAT DELIMITED 
            FIELDS TERMINATED BY ',' 
            STORED AS TEXTFILE;
        """,
    )

    # Create InternetSale table
    create_internet_sale_table = HiveOperator(
        task_id="create_internet_sale_table",
        hive_cli_conn_id="hive_conn",
        hql="""CREATE EXTERNAL TABLE IF NOT EXISTS adventure_works.InternetSale (
                ProductKey INT,
                OrderDateKey STRING,
                DueDateKey STRING,
                ShipDateKey STRING,
                CustomerKey INT,
                SalesOrderNumber STRING,
                SalesAmount DOUBLE
            ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;""",
    )

    # Task to process Customer data
    process_customer = SparkSubmitOperator(
        task_id="process_customer",
        application="/usr/local/airflow/dags/scripts/customer_processing.py",
        conn_id="spark_conn",
        name="process_customer",
        verbose=False,
    )

    # Task to process Product data
    process_product = SparkSubmitOperator(
        task_id="process_product",
        application="/usr/local/airflow/dags/scripts/product_processing.py",
        conn_id="spark_conn",
        name="process_product",
        verbose=False,
    )

    # Task to process Date data
    process_date = SparkSubmitOperator(
        task_id="process_date",
        application="/usr/local/airflow/dags/scripts/date_load.py",
        conn_id="spark_conn",
        name="process_date",
        verbose=False,
    )

    # Task to process InternetSale data
    process_internet_sale = SparkSubmitOperator(
        task_id="process_internet_sale",
        application="/usr/local/airflow/dags/scripts/internetSale_processing.py",
        conn_id="spark_conn",
        name="process_internet_sale",
        verbose=False,
    )

    sending_email_notification = EmailOperator(
        task_id="sending_email",
        to="tranthe748@gmail.com",
        subject="Adventure Works data pipeline",
        html_content="""<h3>adventure_works dag succeeded</h3>""",
    )

    sending_slack_notification = SlackAPIPostOperator(
        task_id="sending_slack",
        slack_conn_id="slack_conn",
        username="airflow",
        text="DAG adventure_works has been successfully completed!",
        channel="#airflow-exploit",
    )

    # File download, upload, and processing workflow
    (
        download_customer_data
        >> check_customer_file
        >> save_customer_to_hdfs
        >> create_adventure_works_schema
        >> create_customer_table
        >> process_customer
    )
    (
        download_product_data
        >> check_product_file
        >> save_product_to_hdfs
        >> create_adventure_works_schema
        >> create_product_table
        >> process_product
    )
    (
        download_date_data
        >> check_date_file
        >> save_date_to_hdfs
        >> create_adventure_works_schema
        >> create_date_table
        >> process_date
    )

    # Workflow for InternetSale data
    (
        download_internet_sale_data
        >> check_internet_sale_file
        >> save_internet_sale_to_hdfs
        >> create_adventure_works_schema
        >> create_internet_sale_table
        >> process_internet_sale
    )

    # Ensure that process_internet_sale runs only after process_customer, process_product, and process_date
    [process_customer, process_product, process_date] >> process_internet_sale

    # Notification workflow
    process_internet_sale >> sending_email_notification >> sending_slack_notification
