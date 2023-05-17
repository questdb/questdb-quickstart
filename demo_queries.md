# Running the demo Queries

If you want to run some interesting queries on top of pre-existing demo datasets, you can head to [QuestDB live demo](https://demo.questdb.io/) and just click on the top where it says 'Example Queries'. The `trips` dataset at that live demo has over 1.6 billion rows. All the datasets at the demo site are static, except for the `trades` table, which pulls crypto prices from Coinbase's API every second or so.


## Performance

We start with number of records

```
select count() from trips:
```

Ask how long they think it’d take and run the next query

```
select count(), avg(fare_amount) from trips;
```

We explain it was ~500ms. Not too bad, but this was a full scan, so no time-series in place. Let’s filter by time

```
select count(), avg(fare_amount) from trips where pickup_datetime IN '2018';
```

```
select count(), avg(fare_amount) from trips where pickup_datetime IN '2018-06';
```

Cool. See how we are getting faster. That’s for performance. Now we switch to business functionality. Lets run this a couple of times to show we are getting new data about every second

## Sample By and interpolation, to group rows by time and to work with missing data

```
select count() from trades;
```

A common business metric would be the volume weighted average every 15 minutes. This is how you can downsample data, by the way, if you just INSERT INTO a new table the result

```
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 15m ALIGN TO CALENDAR;
```

Let’s see what happens if I go down to one second. I can see some seconds are missing! It seems we have some ingestion gaps. Explain conventional databases can only show you what’s inside, but cannot show you what’s NOT inside. But that’s actually super good insights for many use cases. In sensor data you need that all the time

```
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s ALIGN TO CALENDAR;
```

So. Introduce interpolate. You might mention linear and prev, but for identifying gaps I want to use the NULL one

```
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s FILL(NULL) ALIGN TO CALENDAR
```

So I can now see all the rows, including those with no values. How can I see only the anomalies? Easy, as we support SQL and that’s straightforward

```
with sampled as (
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s FILL(NULL) ALIGN TO CALENDAR
) select * from sampled where vwap_price IS NULL
```

We can see if we increase the sample from 1s to 5s, the number of gaps gets smaller, and eventually if we keep increasing, no gaps. A lot of real business cool use cases here

```
with sampled as (
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 5s FILL(NULL) ALIGN TO CALENDAR
) select * from sampled where vwap_price IS NULL
```

```
with sampled as (
SELECT 
    timestamp,
    sum(price * amount) / sum(amount) AS vwap_price,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 10s FILL(NULL) ALIGN TO CALENDAR
) select * from sampled where vwap_price IS NULL
```

## Powerful time semantics using IN

Next, we run the same query but in small steps. We start asking it would be cool to know how many trades we had at one particular second, and we have our handy IN syntax

```
select timestamp, count() from 'trades'
where timestamp IN '2022-10-28T23:59:58'
```

That’s a lot of detail. I want just the count per second, not for each timestamp, so SAMPLE BY again

```
select timestamp, count() from 'trades'
where timestamp IN '2022-10-28T23:59:58'
sample by 1s ALIGN TO CALENDAR
```

Even better, we might want to see what happened in the 2 seconds before and after the top of midnight

```
select timestamp, count() from ‘trades’
where timestamp IN '2022-10-28T23:59:58;4s'
sample by 1s ALIGN TO CALENDAR
```

And what if we want what happened around those seconds for that day and the 7 days afterwards? Yep, more IN syntax. Doing this with other DB would be clunky

```
select timestamp, count() from 'trades'
where timestamp IN '2022-10-28T23:59:58;4s;1d;7'
sample by 1s ALIGN TO CALENDAR
```

## Joining two tables by closer timestamp

Last bit. ASOF JOIN. Weather dataset and trips join at midnight

```
SELECT
  timestamp as weather_timestamp, pickup_datetime, fare_amount, tempF, windDir
FROM
  (
    select * from trips WHERE pickup_datetime in '2018-06-01'
  ) ASOF JOIN weather;
```

And now we change the IN to a different time so we see we are matching a different weather record

```
SELECT
  timestamp as weather_timestamp, pickup_datetime, fare_amount, tempF, windDir
FROM
  (
    select * from trips WHERE pickup_datetime in '2018-06-01T00:55'
  ) ASOF JOIN weather;
  ```
  