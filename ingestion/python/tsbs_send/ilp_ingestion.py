from questdb.ingress import Sender, IngressError, TimestampNanos
import os
import sys
import random
import time

HOST = os.getenv('QDB_CLIENT_HOST', 'localhost')
PORT = os.getenv('QDB_CLIENT_PORT', 9009)
TLS = os.getenv('QDB_CLIENT_TLS', "False" ).lower() in ('true', '1', 't')
AUTH_KID = os.getenv('QDB_CLIENT_AUTH_KID', '')
AUTH_D = os.getenv('QDB_CLIENT_AUTH_D', '')
AUTH_X = os.getenv('QDB_CLIENT_AUTH_X', '')
AUTH_Y = os.getenv('QDB_CLIENT_AUTH_Y', '')

DEVICE_TYPES = ["blue", "red", "green", "yellow"]
ITER = 10000
BATCH = 100
DELAY = 0.5
MIN_LAT = 19.50139
MAX_LAT = 64.85694
MIN_LON = -161.75583
MAX_LON = -68.01197


def send(host: str = HOST, port: int = PORT):
    try:
        auth = None
        if AUTH_KID and AUTH_D and AUTH_X and AUTH_Y:
            sys.stdout.write(f'Ingestion using credentials\n')
            auth = ( AUTH_KID, AUTH_D, AUTH_X, AUTH_Y )
        with Sender(host, port, auth=auth, tls=TLS) as sender:
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
                sys.stdout.write(f'sent : {BATCH} rows\n')
                sender.flush()
                time.sleep(DELAY)
    except IngressError as e:
        sys.stderr.write(f'Got error: {e}')


if __name__ == '__main__':
    sys.stdout.write(f'Ingestion started. Connecting to {HOST} {PORT}\n')
    send()
