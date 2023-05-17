# Ingesting data using JAVA

For ingesting data we are adding QuestDB as a dependency.

The demo program will generate random data simulating IoT sensor data into a table named "ilp_test". Note we don't need to create the table beforehand, as QuestDB will automatically create a table, if it doesn't already exist, when we start sending data.

This demo will generate and ingest 100,000 events in batches of 100 events every 500 milliseconds. You can interrupt the program at any point while executing without any side effects.

## Getting the dependencies

Change directory to `tsbs_send`

Generate the `jar` and dependencies with `maven`

`mvn clean package`

## Running the program

`java -jar target/ilp_ingestion-1.0-SNAPSHOT.jar`

## Validating we ingested some data

Go to the webconsole (http://localhost:9000 if running locally) and execute this query

`Select * from ilp_test`

Then

`Select count() from ilp_test`

You can leave the JAVA program running while you proceed to the last step of this quickstart and visualise your data on a dashboard.
