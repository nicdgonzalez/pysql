from __future__ import annotations

from typing import TYPE_CHECKING

from .column import NamedColumn
from .statement import Statement

if TYPE_CHECKING:
    from typing import Any, Mapping

    from .model import Model


class Table:
    def __init__(
        self,
        *,
        name: str,
        columns: list[NamedColumn],
        inherit_from: Table | None = None,
    ) -> None:
        self._name = name
        self._columns = columns
        self._column_names = set((c.name for c in self._columns))
        self.inherit_from = inherit_from

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> list[NamedColumn]:
        return self._columns

    @property
    def column_names(self) -> set[str]:
        return self._column_names

    def create(self) -> Statement:
        assert all((isinstance(c, NamedColumn) for c in self.columns))
        columns = [c.to_sql_definition() for c in self.columns]

        primary_keys = [c.name for c in self.columns if c.primary_key is True]
        columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

        query = (
            f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join(columns)})"
        )

        if self.inherit_from is not None:
            query += f" INHERITS ({self.inherit_from.name})"

        return Statement(query)

    def insert(self, model: Model) -> Statement:
        placeholders = ("%s" for _ in range(len(model.record.keys())))
        query = (
            f"INSERT INTO {self.name}({', '.join(model.record.keys())}) "
            f"VALUES({', '.join(placeholders)})"
        )
        return Statement(query, tuple(model.record.values()))

    def update(
        self,
        model: Model,
        *,
        filter: Mapping[str, Any] | None = None,
    ) -> Statement:
        changes: list[str] = [f"{c} = %s" for c in model.record.keys()]
        query = f"UPDATE {self.name} SET {', '.join(changes)}"
        values = list(model.record.values())

        if filter is not None:
            conditions: list[str] = []

            for column, value in filter.items():
                conditions.append(f"{column} = %s")
                values.append(value)

            query += f" WHERE {' AND '.join(conditions)}"

        return Statement(query, tuple(values))

    def delete(self, filter: Model | None) -> Statement:
        query = f"DELETE FROM {self.name}"
        values: list[Any] = []

        if filter.record is not None:
            conditions: list[str] = []

            for column, value in filter.record.items():
                conditions.append(f"{column} = %s")
                values.append(value)

            query += f" WHERE {' AND '.join(conditions)}"

        return Statement(query, tuple(values))

    def fetch(
        self,
        *,
        select: list[str],
        filter: Model | None = None,
    ) -> Statement:
        query = f"SELECT {', '.join(select)} FROM {self.name}"
        values: list[Any] = []

        if filter is not None:
            conditions: list[str] = []

            for column, value in filter.record.items():
                conditions.append(f"{column} = %s")
                values.append(value)

            query += f" WHERE {' AND '.join(conditions)}"

        return Statement(query, tuple(values))
