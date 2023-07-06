import psycopg as pg
from faker import Faker
from faker.providers import DynamicProvider
from faker.providers import internet
import os
import sys

HOST = os.getenv('QDB_CLIENT_HOST', '127.0.0.1')
PORT = os.getenv('QDB_CLIENT_PORT', 8812)
PG_USER = os.getenv('QDB_CLIENT_PG_USER', 'admin')
PG_PASSWORD = os.getenv('QDB_CLIENT_PG_PASSWORD', 'quest')


def get_fake_generator():
    app_actions_provider = DynamicProvider(
     provider_name="app_action",
     elements=[
        "/login",
        "/stock/buy",
        "/stock/sell",
        "/stock/check",
        "/user/profile",
        "contract/download"
        ],
)
    fake_generator = Faker()
    fake_generator.add_provider(app_actions_provider)
    fake_generator.add_provider(internet)

    return fake_generator

def fake_row(fake_generator):
    row=dict()
    profile = fake_generator.profile()
    row['name'] = profile['name']
    row['user_name'] = profile['username']
    row["email"] = profile['mail']
    row['company'] = profile['company']
    row['app_action'] = fake_generator.app_action()
    row['credit_card_provider'] = 'NULL'
    if row['app_action'] == "/stock/buy":
        row['credit_card_provider'] = fake_generator.credit_card_provider()
    row['file_name'] = 'NULL'
    if row['app_action'] == "contract/download":
        row['file_name'] = fake_generator.file_path(extension='pdf')
    row['ip']=fake_generator.ipv4_private()
    row['method']=fake_generator.http_method()
    row['user_agent']=fake_generator.user_agent()
    row['country_code'] = fake_generator.country_code()
    row['time_ms'] = fake_generator.pyint(min_value=20, max_value=1500)
    row['error'] = fake_generator.pybool(truth_probability=8)
    return row

if __name__ == '__main__':
   conn_str = f'user={PG_USER} password={PG_PASSWORD} host={HOST} port={PORT} dbname=qdb'
   with pg.connect(conn_str, autocommit=True) as connection:
        with connection.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS app_monitor(
                name STRING,
                username SYMBOL capacity 256 CACHE,
                email STRING,
                company STRING,
                app_action SYMBOL capacity 10 CACHE,
                credit_card_provider SYMBOL capacity 10 CACHE,
                file_name STRING,
                ip STRING,
                method SYMBOL capacity 10 CACHE,
                user_agent SYMBOL capacity 50 CACHE,
                country_code SYMBOL capacity 150 CACHE,
                time_ms LONG,
                timestamp TIMESTAMP
                ) TIMESTAMP (timestamp) PARTITION BY DAY WAL;
            '''
            )

            fg = get_fake_generator()
            print(fake_row(fg))


