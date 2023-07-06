import psycopg as pg
import yliveticker
import os
import sys

HOST = os.getenv('QDB_CLIENT_HOST', '127.0.0.1')
PORT = os.getenv('QDB_CLIENT_PORT', 8812)
PG_USER = os.getenv('QDB_CLIENT_PG_USER', 'admin')
PG_PASSWORD = os.getenv('QDB_CLIENT_PG_PASSWORD', 'quest')

def on_new_row(ws, msg):
    with pg.connect(yliveticker.conn_str, autocommit=True) as connection:
        msg['timestamp'] =  msg['timestamp'] * 1000
        with connection.cursor() as cur:
            cur.execute('''
            INSERT INTO live_ticker(
                id,
                exchange,
                quoteType,
                price,
                marketHours,
                changePercent,
                dayVolume,
                change,
                priceHint,
                timestamp
                )
                VALUES(
                    %(id)s,
                    %(exchange)s,
                    %(quoteType)s,
                    %(price)s,
                    %(marketHours)s,
                    %(changePercent)s,
                    %(dayVolume)s ,
                    %(change)s,
                    %(priceHint)s,
                    %(timestamp)s  );
                '''
            , msg
            )
    sys.stdout.write(f'sent : {msg}\n')

def get_ticker_names():
    with open('ticker_names.txt') as f:
        lines = f.read().splitlines()
    return list(set(lines))


if __name__ == '__main__':
    yliveticker.conn_str = f'user={PG_USER} password={PG_PASSWORD} host={HOST} port={PORT} dbname=qdb'
    with pg.connect(yliveticker.conn_str, autocommit=True) as connection:
        with connection.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS live_ticker(
                'id' SYMBOL capacity 256 CACHE,
                exchange SYMBOL capacity 256 CACHE,
                quoteType LONG,
                price DOUBLE,
                marketHours LONG,
                changePercent DOUBLE,
                dayVolume DOUBLE,
                change DOUBLE,
                priceHint LONG,
                timestamp TIMESTAMP
                ) TIMESTAMP (timestamp) PARTITION BY DAY WAL;
            '''
            )

    yliveticker.YLiveTicker(on_ticker=on_new_row, ticker_names=get_ticker_names())
