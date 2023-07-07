# Ingesting data using Python

We provide three different scripts to ingest data into QuestDB:

* ilp_ingestion: simulates IoT data using the ILP protocol. It only requires the questdb library. This script is also available in the Go and JAVA samples. The
demo Grafana dashboard provided in this quickstart works on this table
* app_monitoring_ingestion: simulates app observability data using the PostgreSQL protocol. It requires the psycopg and the faker libraries
* ticker_ingestion: reads real live data from Yahoo Finance and inserts into QuestDB using the PostgreSQL protocol. It requires the psycopg and the yliveticker libraries

You can install each dependency manually using `pip`, or just all of them via

`cd tsbs_send`
`pip install -r requirements.txt`

## IoT simulated data: ilp_ingestion.py demo

The demo program will generate random data simulating IoT sensor data into a table named "ilp_test". Note we don't need to create the table beforehand, as QuestDB will automatically create a table, if it doesn't already exist, when we start sending data.

This demo will generate and ingest 100,000 events in batches of 100 events every 500 milliseconds. You can interrupt the program at any point while executing without any side effects.

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (or to run with TLS if using the QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to 'localhost'
* QDB_CLIENT_PORT, defaults to 9009
* QDB_CLIENT_TLS, defaults to False
* QDB_CLIENT_AUTH_KID, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console
* QDB_CLIENT_AUTH_D, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console
* QDB_CLIENT_AUTH_X, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console
* QDB_CLIENT_AUTH_Y, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console

### Running the program

`python ilp_ingestion.py`

### Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from ilp_test`

Then

`Select count() from ilp_test`

You can leave the Python program running while you proceed to the last step of this quickstart and visualise your data on a dashboard.

## App observability simulated data: app_monitoring_ingestion.py demo

This demo program will generate random data (using the Faker library) simulating application usage data into a table named "app_monitor".
Data is ingested using the pg_wire protocol. Note we don't need to create the table beforehand, as the script starts with a call to `CREATE TABLE IT NOT EXISTS`.

This demo will generate one row every 100 milliseconds until stopped. You can interrupt the program at any point while executing without any side effects.

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (including QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to '127.0.0.1'
* QDB_CLIENT_PORT, defaults to 8812
* QDB_CLIENT_PG_USER, defaults to 'admin'
* QDB_CLIENT_PG_PASSWORD, defaults to 'quest'

### Running the program

`python app_monitoring_ingestion.py`

### Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from app_monitor`

Then

`Select count() from app_monitor`


## App observability simulated data: app_monitoring_ingestion.py demo

This demo program will generate random data (using the Faker library) simulating application usage data into a table named "app_monitor".
Data is ingested using the pg_wire protocol. Note we don't need to create the table beforehand, as the script starts with a call to `CREATE TABLE IT NOT EXISTS`.

This demo will generate one row every 100 milliseconds until stopped. You can interrupt the program at any point while executing without any side effects.

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (including QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to '127.0.0.1'
* QDB_CLIENT_PORT, defaults to 8812
* QDB_CLIENT_PG_USER, defaults to 'admin'
* QDB_CLIENT_PG_PASSWORD, defaults to 'quest'

### Running the program

`python app_monitoring_ingestion.py`

### Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from app_monitor`

Then

`Select count() from app_monitor`


## App observability simulated data: app_monitoring_ingestion.py demo

This demo program will generate random data (using the Faker library) simulating application usage data into a table named "app_monitor".
Data is ingested using the pg_wire protocol. Note we don't need to create the table beforehand, as the script starts with a call to `CREATE TABLE IT NOT EXISTS`.

This demo will generate one row every 100 milliseconds until stopped. You can interrupt the program at any point while executing without any side effects.

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (including QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to '127.0.0.1'
* QDB_CLIENT_PORT, defaults to 8812
* QDB_CLIENT_PG_USER, defaults to 'admin'
* QDB_CLIENT_PG_PASSWORD, defaults to 'quest'

### Running the program

`python app_monitoring_ingestion.py`

### Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from app_monitor`

Then

`Select count() from app_monitor`


## Live financial data from Yahoo Finance: ticker_ingestion.py demo

This demo program will read live data (using the yliveticker library) from Yahoo Finance websocket and ingest into a table named "live_ticker".
Data is ingested using the pg_wire protocol. Note we don't need to create the table beforehand, as the script starts with a call to `CREATE TABLE IT NOT EXISTS`.

This demo will generate data as it comes (volume depends on market hours, but at most it generates a few records per second) until stopped.
You can interrupt the program at any point while executing without any side effects.

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (including QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to '127.0.0.1'
* QDB_CLIENT_PORT, defaults to 8812
* QDB_CLIENT_PG_USER, defaults to 'admin'
* QDB_CLIENT_PG_PASSWORD, defaults to 'quest'

The program will read the file `ticker_names.txt` on start, and will monitor all the tickers there. By default it is monitoring exchange between some currencies,
and some tickers in US, India, Japan, and Spanish markets, so there is some activity most of the time independently of market opening/close hours.
If you want to change the file or to add your own tickets, you can get the ticker name from the `https://finance.yahoo.com/` website. Notice the ticker needs to
have the exact format from Yahoo's website (including any preffixes or suffixes) so we can match it. You need to add a ticker per line with no spaces before or after.

### Running the program

`python ticker_ingestion.py`

### Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from live_ticker`

Then

`Select count() from live_ticker`
