# questdb-quickstart

QuestDB is an Apache 2.0 licensed time-series database for high throughput ingestion and fast SQL queries with operational simplicity. To learn more about QuestDB visit https://questdb.io

 This is a quickstart covering:

* Getting started with QuestDB on docker
* Loading data using a CSV
* Using the web console for interactive queries
* Ingesting real-time data using the official clients in Go, Java, or Python
* Real-time dashboards with Grafana and QuestDB using the PostgreSQL connector

# Deploying the demo

This quickstart requires starting or deploying QuestDB, Grafana, and some ingestion scripts. You have three ways of setting this up:

* Fully managed cloud-based installation (requires creating a free account on gitpod) using the Gitpod link in the next section. Recommended for quick low-friction demo
* Local installation using docker-compose. Recommended for quick low-friction demo, as long as you have docker/docker-compose installed locally and are comfortable using them
* Local installation using docker but doing step-by-step. Recommended to learn more about the details and how everything fits together


After you install with your preferred method (instructions below) you can proceed to (loading and querying data)[./loading_and_querying_data.md]

## Fully managed deployment using Gitpod

When you click the button below, gitpod will provision an environment with questdb, a python script generating demo data,
and a grafana dashboard for visualisation. On finishing (typically about one minute), gitpod will try to open two new
tabs, one with the grafana dashboard, one with the QuestDB web interface. When opening the grafana dashboard,
user is "demo" and password is "quest".

Click the button below to start a new development environment:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/questdb/questdb-quickstart)

Note: If you already have a gitpod account, you will need to log in when launching the deployment. If you don't have a gitpod
account, you can create one for free when launching the deployment. If your browser is blocking pop-ups, you will
need to click on the alert icon on the navigation bar to open the two links after the deployment is complete.

## Docker-compose local deployment

Docker compose will provision an environment with questdb, a python script generating demo data,
and a grafana dashboard for visualisation. The whole process will take about 2-3 minutes, depending on yout internet speed
downloading the container images, and how quick your machine can build a python-based docker image.

```
git clone https://github.com/questdb/questdb-quickstart.git
cd questdb-quickstart
docker-compose up
```

The grafana web interface will be available at http://localhost:13000/d/qdb-ilp-demo/device-data-questdb-demo?orgId=1&refresh=5s.
User is "demo" and password is "quest".

The QuestDB console is available at http://localhost:19000

Stop the demo via:

```
docker-compose down
```

## Local docker based deployment

There are [many ways to install QuestDB](https://questdb.io/docs/get-started/docker/), but I am choosing docker for portability. Note I won't be using a docker volume and the data will be ephemeral. Check the QuestDB docks to see how to start with a persistent directory.

```docker run --add-host=host.docker.internal:host-gateway -p 9000:9000 -p 9009:9009 -p 8812:8812 -p 9003:9003 questdb/questdb:latest```

Port 9000 serves the web console, port 9009 is for streaming ingestion, port 8812 is for PostgreSQL-protocol reads or writes, port 9003 is a monitoring/metrics endpoint



