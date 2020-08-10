import pickle
import sqlite3
from typing import Dict
from state import Aria


def connect(path: str = "database.sqlite3") -> sqlite3.Connection:
    return sqlite3.connect(path)


def create_schema(connection: sqlite3.Connection) -> None:
    c = connection.cursor()
    try:
        c.execute(
            "CREATE TABLE IF NOT EXISTS states (user_id INTEGER UNIQUE NOT NULL, data BYTES NOT NULL)"
        )
        connection.commit()
    finally:
        c.close()


def to_database(state: Aria, connection: sqlite3.Connection) -> None:
    c = connection.cursor()
    try:
        payload = pickle.dumps(state)
        c.execute(
            "INSERT INTO states (user_id, data) VALUES (?, ?)", (state.user_id, payload)
        )
        connection.commit()
    finally:
        c.close()


def from_database(user_id: int, connection: sqlite3.Connection) -> Aria:
    c = connection.cursor()
    try:
        c.execute("SELECT data FROM states WHERE user_id = ?", (user_id,))
        (data,) = c.fetchone()
        return pickle.loads(data)
    finally:
        c.close()

def load_all() -> Dict[int, Aria]:
    with connect() as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT data, user_id FROM states")
            results = {}
            for (data, user_id) in c:
                results[user_id] = pickle.loads(data)

            return results
        finally:
            c.close()