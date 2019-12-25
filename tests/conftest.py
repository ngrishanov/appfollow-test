import asyncio
import time

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
import pytest

from appfollow_test import config


POSTGRES_SUPER_USER = config.POSTGRES_USER
POSTGRES_SUPER_PASSWORD = config.POSTGRES_PASSWORD
POSTGRES_SUPER_DB = config.POSTGRES_DB
POSTGRES_SUPER_HOST = config.POSTGRES_HOST
POSTGRES_SUPER_PORT = config.POSTGRES_PORT

POSTGRES_TEST_DB = config.POSTGRES_TEST_DB_TEMPLATE.format(config.POSTGRES_DB)
config.POSTGRES_DB = POSTGRES_TEST_DB


from appfollow_test.app import app as application  # noqa


def setup_db():
    attempts = 10
    while True:
        try:
            conn = psycopg2.connect(
                user=POSTGRES_SUPER_USER,
                password=POSTGRES_SUPER_PASSWORD,
                dbname=POSTGRES_SUPER_DB,
                host=POSTGRES_SUPER_HOST,
                port=POSTGRES_SUPER_PORT,
            )
            break
        except psycopg2.OperationalError as e:
            attempts -= 1
            if not attempts:
                raise e
            time.sleep(1)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        cursor.execute(f'CREATE DATABASE "{POSTGRES_TEST_DB}" OWNER "{config.POSTGRES_USER}";')
    except psycopg2.ProgrammingError:
        cursor.execute(f'DROP DATABASE "{POSTGRES_TEST_DB}";')
        cursor.execute(f'CREATE DATABASE "{POSTGRES_TEST_DB}" OWNER "{config.POSTGRES_USER}";')

    cursor.close()
    conn.close()

    # apply schema

    conn = psycopg2.connect(
        user=POSTGRES_SUPER_USER,
        password=POSTGRES_SUPER_PASSWORD,
        dbname=POSTGRES_TEST_DB,
        host=POSTGRES_SUPER_HOST,
        port=POSTGRES_SUPER_PORT,
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    with open('../schema.sql') as f:
        cursor.execute(f.read())

    cursor.close()
    conn.close()


def teardown_db():
    conn = psycopg2.connect(
        user=POSTGRES_SUPER_USER,
        password=POSTGRES_SUPER_PASSWORD,
        dbname=POSTGRES_SUPER_DB,
        host=POSTGRES_SUPER_HOST,
        port=POSTGRES_SUPER_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute(f'DROP DATABASE "{POSTGRES_TEST_DB}"')

    cursor.close()
    conn.close()


@pytest.fixture(scope='function', autouse=True)
def database():
    setup_db()
    yield
    teardown_db()


# noinspection PyShadowingNames
@pytest.fixture()
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# noinspection PyShadowingNames
@pytest.fixture()
def loop(event_loop):
    return event_loop


@pytest.yield_fixture
def app():
    yield application


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
