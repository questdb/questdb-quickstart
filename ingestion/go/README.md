# Ingesting data using go

For ingesting data we are using the official QuestDB Go client.

The demo program will generate random data simulating IoT sensor data into a table named "ilp_test". Note we don't need to create the table beforehand, as QuestDB will automatically create a table, if it doesn't already exist, when we start sending data.

This demo will generate and ingest 100,000 events in batches of 100 events every 500 milliseconds. You can interrupt the program at any point while executing without any side effects.

## Getting the dependencies

Change directory to `tsbs_send`
This will download the go questdb package

`go mod download github.com/questdb/go-questdb-client`

### Configuration

It defaults to localhost with all the QuestDB defaults, but can be adapted to use different credentials (or to run with TLS if using the QuestDB Cloud) by setting these environment variables:
* QDB_CLIENT_HOST, defaults to 'localhost'
* QDB_CLIENT_PORT, defaults to 9009
* QDB_CLIENT_TLS, defaults to False
* QDB_CLIENT_AUTH_KID, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console
* QDB_CLIENT_AUTH_D, no default. Only used for authenticated ILP. You can find this param on your QuestDB Cloud instance console

## Running the program

`go run src/main_orig.go`

## Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from ilp_test`

Then

`Select count() from ilp_test`

You can leave the go program running while you proceed to the last step of this quickstart and visualise your data on a dashboard.
