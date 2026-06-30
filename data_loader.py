import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple

Record = Dict[str, Any]


class DataSource(ABC):
    """Abstraction over a source of records."""

    @abstractmethod
    def read(self) -> List[Record]:
        """Return the records to be loaded."""


class JsonFileDataSource(DataSource):
    """Reads a list of records from a JSON file."""

    def __init__(self, path: str) -> None:
        self._path = path

    def read(self) -> List[Record]:
        with open(self._path, "r", encoding="utf-8") as file:
            return json.load(file)


@dataclass(frozen=True)
class TableMapping:
    """Describes how a record maps onto a database table.

    ``conflict_columns`` names the primary-key / unique columns used to detect
    a conflict. When set, the generated statement becomes an upsert
    (``ON CONFLICT ... DO UPDATE``); when empty it is a plain ``INSERT``.
    """

    table: str
    columns: Sequence[str]
    conflict_columns: Sequence[str] = ()

    @property
    def statement(self) -> str:
        placeholders = ", ".join(["%s"] * len(self.columns))
        column_list = ", ".join(self.columns)
        statement = (
            f"INSERT INTO {self.table} ({column_list}) VALUES ({placeholders})"
        )
        if not self.conflict_columns:
            return statement

        conflict = ", ".join(self.conflict_columns)
        updatable = [c for c in self.columns if c not in self.conflict_columns]
        if updatable:
            assignments = ", ".join(f"{c} = EXCLUDED.{c}" for c in updatable)
            return f"{statement} ON CONFLICT ({conflict}) DO UPDATE SET {assignments}"
        return f"{statement} ON CONFLICT ({conflict}) DO NOTHING"

    def row(self, record: Record) -> Tuple[Any, ...]:
        return tuple(record[column] for column in self.columns)


class DataLoader:
    """Loads records from a :class:`DataSource` into a mapped table."""

    def __init__(self, connection) -> None:
        self._connection = connection

    def load(self, source: DataSource, mapping: TableMapping) -> int:
        """Insert every record from ``source`` into ``mapping``'s table.

        Returns the number of rows inserted. Lets database/IO errors propagate
        so the caller can decide how to handle a failed load.
        """
        rows = [mapping.row(record) for record in source.read()]
        cursor = self._connection.cursor()
        cursor.executemany(mapping.statement, rows)
        self._connection.commit()
        return cursor.rowcount


# Declarative mappings — add new entities here without touching DataLoader.
ROOMS = TableMapping(
    table="rooms",
    columns=("id", "name"),
    conflict_columns=("id",),
)
STUDENTS = TableMapping(
    table="students",
    columns=("id", "name", "birthday", "room", "sex"),
    conflict_columns=("id",),
)
