# Loading and Querying data

Make sure you have a working QuestDB installation as explained at the [README](./README.md)

## Loading data using a CSV

There are different ways of loading CSV data into QuestDB. I am showing here the simplest one, recommended only for small/medium files with rows sorted by timestamp.

Go to the url of the web console, which runs on port 9000. If you are running this on your machine, it should be running at http://localhost:9000

You will see some icons at the left bar. Choose the one with an arrow pointing up. When you hover it will read "import". Click to browse or drag the provided demo file `trips.csv` at the [root of this repository](./trips.csv). After a few seconds, your file should be loaded.

Go back to the web console main screen by clicking the `</>` icon on the left menu bar.


## Using the web console for interactive queries

If the name `trips.csv` is not showing at the `tables` section, click the reload icon (a circle formed by two arrows) at the top left.

You can now click on the table name to see the auto-discovered schema.

Run your first query by writting `select * from 'trips.csv'` at the editor and click run.

The data we loaded represents real taxi rides in the city of New York in January 2018. It is a very small dataset with only 999 rows for demo purposes.

Since the name of the table is not great, let's rename it by running this SQL statement

`rename table 'trips.csv' to  trips_2018`

And now we can run queries like

`select count() from trips_2018`

You can find the complete SQL reference for QuestDB (including time-series extensions) at [the docs](https://questdb.io/docs/concept/sql-execution-order/)

If you want to run some interesting queries on top of larger demo datasets, you can head to [QuestDB live demo](https://demo.questdb.io/) and just click on the top where it says 'Example Queries'. The `trips` dataset at that live demo has over 1.6 billion rows. All the datasets at the demo site are static, except for the `trades` table, which pulls crypto prices from Coinbase's API every second or so.

I have compiled some of the queries you can run on the demo dataset in [this markdown file](./demo_queries.md)

## Loading CSV data using the API

We can also load CSV files using the API. In this case, we can add schema details (for every column or just specific ones),
and table details, such as the name, or the partitioning strategy.

In this repository, I am providing a dataset with energy consumption and forecast data in 15-minutes intervals for a few
European countries. This file is a subset of [the original](https://data.open-power-system-data.org/time_series/2020-10-06)
and contains data only for 2018 (205,189 rows).

Import using curl:

```
curl -F schema='[{"name":"timestamp", "type": "TIMESTAMP", "pattern": "yyyy-MM-dd HH:mm:ss"}]' -F data=@energy_2018.csv 'http://localhost:9000/imp?overwrite=false&name=energy_2018&timestamp=timestamp&partitionBy=MONTH'
```

Navigate to the [QuestDB Web Console](http://localhost:9000) and explore the table we just created.



