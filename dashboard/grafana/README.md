# Building a Grafana dashboard

We will use Grafana, a popular open source tool for dashboards, to connect to your QuestDB instance and displaying near real time dashboards. We will use the grafana postgresql connector to connect to QuestDB.

## Installing grafana via docker

If you still don't have a local grafana, you can start one with a persistent volume

### create a persistent volume for your data in /var/lib/grafana (database and plugins)
docker volume create grafana-storage

### start grafana
docker run --add-host=host.docker.internal:host-gateway -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana grafana/grafana-oss

## Creating the connection to QuestDB

Go to http://localhost:3000 and log into your local Grafana instllation.

In your grafana, find the data sources icon at the left menu and add a new one. Choose the PostgreSQL type. 

You can enter any name you want, for example `qdb`, for host you need to enter `host.docker.internal:8812`. If you are running Grafana without docker, just use `localhost:8812`. For database choose `qdb`, user `admin`, password `quest`. Those are all default values that could be changed, but we are using just the defaults for this demo.

Out of the box, QuestDB doesn't have TLS/SSL support, so we need to select `disable` for TLS/SSL Mode.

Scroll down to the bottom of the screen and click on `Save & Test`. You should see the connection is working.

## Importing the dashboard

We are providing a pre-configured Grafana dashboard (`DeviceData-QuestDBCloudDemo.json`) in this repository. To import it, find the dashboard>import option at the left menu of your local grafana, and then select the json file. Grafana will ask you to select a PostgreSQL connection. Choose the one we just created.

The dashboard should be ready and, if you are ingesting data, you should now see live data being updated.
