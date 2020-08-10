import os
from database import connect, create_schema, from_database, to_database
from state import Aria

DB = "test.sqlite3"


def setup_module(module):
    conn = connect(DB)
    create_schema(conn)


def teardown_module(module):
    try:
        os.remove(DB)
    except IOError as e:
        print(e)


def test_to_database():
    aria = Aria(12, "username")
    conn = connect(DB)

    to_database(aria, conn)

    from_db = from_database(12, conn)
    assert aria == from_db

    conn.close()
