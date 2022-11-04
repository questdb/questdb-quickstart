# questdb-quickstart

QuestDB is an Apache 2.0 licensed time-series database for high throughput ingestion and fast SQL queries with operational simplicity. To learn more about QuestDB visit https://questdb.io

 This is a quickstart covering:

* Getting started with QuestDB on docker
* Loading data using a CSV
* Using the web console for interactive queries
* Ingesting real-time data using the official clients in Go, Java, or Python
* Real-time dashboards with Grafana and QuestDB using the PostgreSQL connector 


## Getting started with QuestDB on docker

There are [many ways to install QuestDB](https://questdb.io/docs/get-started/docker/), but I am choosing docker for portability. Note I won't be using a docker volume and the data will be ephemeral. Check the QuestDB docks to see how to start with a persistent directory.

```docker run --add-host=host.docker.internal:host-gateway -p 9000:9000 -p 9009:9009 -p 8812:8812 -p 9003:9003 questdb/questdb:latest```

Port 9000 serves the web console, port 9009 is for streaming ingestion, port 8812 is for PostgreSQL-protocol reads or writes, port 9003 is a monitoring/metrics endpoint

## Loading data using a CSV

There are different ways of loading CSV data into QuestDB. I am showing here the simplest one, recommended only for small/medium files with rows sorted by timestamp.

Go to the url of the web console, which runs on port 9000. If you are running this on your machine, it should be running at http://localhost:9000

You will see some icons at the left bar. Choose the one with an arrow pointing up. When you hover it will read "import". Click to browse or drag the provided demo file `trips.csv`. After a few seconds, your file should be loaded.

Go back to the web console main screen by clicking the `</>` icon on the left menu bar.


## Using the web console for interactive queries

If the name `trips.csv` is not showing at the `tables` section, click the reload icon (a circle formed by two arrows) at the top left. 

You can now click on the table name to see the auto-discovered schema.

Run your first query by writting `select * from 'trips.csv'` at the editor and click run.

The data we loaded represents real taxi rides in the city of New York in January 2018. It is a very small dataset with only 999 rows for demo purposes.

Since the name of the table is not great, let's rename it by running this SQL statement

`rename table 'trips.csv' to  trips`

And now we can run queries like

`select count() from trips`

You can find the complete SQL reference for QuestDB (including time-series extensions) at [the docs](https://questdb.io/docs/concept/sql-execution-order/)

If you want to run some interesting queries on top of larger demo datasets, you can head to [QuestDB live demo](https://demo.questdb.io/) and just click on the top where it says 'Example Queries'. The `trips` dataset at that live demo has over 1.6 billion rows. All the datasets at the demo site are static, except for the `trades` table, which pulls crypto prices from Coinbase's API every second or so.

## Ingesting real-time data using the official clients in Go, Java, or Python

Follow the instructions at https://github.com/javier/questdb-quickstart/tree/main/ingestion/go


## Real-time dashboards with Grafana and QuestDB using the PostgreSQL connector 

Follow the instructions at https://github.com/javier/questdb-quickstart/tree/main/dashboard/grafana

