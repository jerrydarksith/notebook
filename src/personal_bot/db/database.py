from collections.abc import Sequence
from pathlib import Path
import sqlite3


class Database:
    """The only class responsible for communicating with SQLite."""

    def __init__(self, database_path: Path) -> None:
        database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(database_path)
        self._connection.execute("PRAGMA foreign_keys = ON")

    def execute(
        self,
        statement: str,
        parameters: Sequence[object] = (),
    ) -> sqlite3.Cursor:
        return self._connection.execute(statement, parameters)

    def execute_script(self, script: str) -> None:
        self._connection.executescript(script)

    def close(self) -> None:
        self._connection.close()

