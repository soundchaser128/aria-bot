import os
from database import Database
from state import Aria

DB = "test.sqlite3"


def setup_module(module):
    db = Database(DB)
    db.create_schema()

def teardown_module(module):
    try:
        os.remove(DB)
    except IOError as e:
        print(e)


def test_to_database():
    aria = Aria(12, "username")
    db = Database(DB)
    db.save_state(aria)

    from_db = db.load_state(12)
    assert from_db == aria
