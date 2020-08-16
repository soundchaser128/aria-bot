import pickle
import sqlite3
from sqlite3.dbapi2 import Cursor
from typing import Callable, Dict
from state import Aria
from contextlib import closing


class Database:
    connection: sqlite3.Connection

    def __init__(self, path: str = "database.sqlite3") -> None:
        self.connection = sqlite3.connect(path)

    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()

    def create_schema(self) -> None:
        with closing(self.cursor()) as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS states (user_id INTEGER UNIQUE NOT NULL, data BYTES NOT NULL)"
            )
            self.connection.commit()

    def save_state(self, state: Aria) -> None:
        with closing(self.cursor()) as cursor:
            payload = pickle.dumps(state)
            cursor.execute(
                "INSERT INTO states (user_id, data) VALUES (?, ?)",
                (state.user_id, payload),
            )
            self.connection.commit()

    def load_state(self, user_id: int) -> Aria:
        with closing(self.cursor()) as cursor:
            cursor.execute("SELECT data FROM states WHERE user_id = ?", (user_id,))
            (data,) = cursor.fetchone()
            return pickle.loads(data)

    def load_states(self) -> Dict[int, Aria]:
        with closing(self.cursor()) as cursor:
            cursor.execute("SELECT data, user_id FROM states")
            results = {}
            for (data, user_id) in cursor:
                results[user_id] = pickle.loads(data)
            return results
