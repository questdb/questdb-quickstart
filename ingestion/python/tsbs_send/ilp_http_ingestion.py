from questdb.ingress import Sender, IngressError, TimestampNanos, Protocol
import os
import sys
import random
import time

CONF_STRING=os.getenv('QDB_CLIENT_CONF', 'http::addr=localhost:9000;username=admin;password=quest;')

DEVICE_TYPES = ["blue", "red", "green", "yellow"]
ITER = 10000
BATCH = 10000
DELAY = 0 
MIN_LAT = 19.50139
MAX_LAT = 64.85694
MIN_LON = -161.75583
MAX_LON = -68.01197


def send(conf: str = CONF_STRING):
    try:
        with Sender.from_conf(conf) as sender:
            for it in range(ITER):
                for i in range(BATCH):
                    sender.row(
                        'ilp_test',
                        symbols={'device_type': random.choice(DEVICE_TYPES)},
                        columns={
                                    'duration_ms': random.randint(0, 4000),
                                    "lat": random.uniform(MIN_LAT, MAX_LAT),
                                    "lon": random.uniform(MIN_LON, MAX_LON),
                                    "measure1": random.randint(-2147483648, 2147483647),
                                    "measure2": random.randint(-2147483648, 2147483647),
                                    "speed": random.randint(0, 100)
                        },
                        at=TimestampNanos.now())
                sys.stdout.write(f'added : {BATCH} rows\n')
                time.sleep(DELAY)
    except IngressError as e:
        sys.stderr.write(f'Got error: {e}')


if __name__ == '__main__':
    sys.stdout.write(f'Ingestion started. Connecting to {CONF_STRING}\n')
    send()
