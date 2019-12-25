HN_URL = 'https://news.ycombinator.com'
HN_PARSE_INTERVAL = 60

POSTGRES_USER = 'appfollow-test'
POSTGRES_PASSWORD = 'appfollow-test'
POSTGRES_DB = 'appfollow-test'
POSTGRES_HOST = 'postgres'
POSTGRES_PORT = '5432'

POSTGRES_TEST_DB_TEMPLATE = 'test-{}'


def get_postgres_dsn():
    return f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
