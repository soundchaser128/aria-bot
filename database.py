from state import Aria
import pickle
import sqlite3


def connect(path: str = "database.sqlite3") -> sqlite3.Connection:
    return sqlite3.connect(path)


def create_schema(connection: sqlite3.Connection) -> None:
    c = connection.cursor()
    try:
        c.execute(
            "CREATE TABLE IF NOT EXISTS states (user_id INTEGER UNIQUE NOT NULL, data BYTES NOT NULL)"
        )
        connection.commit()
    except:
        c.close()


def to_database(state: Aria, connection: sqlite3.Connection) -> None:
    c = connection.cursor()
    try:
        payload = pickle.dumps(state)
        c.execute(
            "INSERT INTO states (user_id, data) VALUES (?, ?)", (state.user_id, payload)
        )
        connection.commit()
    except:
        c.close()


def from_database(user_id: int, connection: sqlite3.Connection) -> Aria:
    c = connection.cursor()
    try:
        c.execute("SELECT data FROM states WHERE user_id = ?", (user_id,))
        (data,) = c.fetchone()
        return pickle.loads(data)
    except:
        c.close()
