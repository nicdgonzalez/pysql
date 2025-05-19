from __future__ import annotations

from typing import TYPE_CHECKING

from .column import Column
from .statement import Statement

if TYPE_CHECKING:
    from typing import Any, Dict, Iterable, List, Optional

    from .model import Model
    from .schema import Schema

__all__: List[str] = [
    "Table"
]


class Table:
    """Represents a schema table in the database."""

    schema: Schema  # The schema this table belongs to.

    def __init__(
        self,
        __name: str,
        /,
        schema: Schema,
        columns: Iterable[Column] = [],
        constraints: Optional[Iterable[str]] = [],
        inherit_from: Optional[Table] = None
    ) -> None:

        self.unaltered_name: str = __name
        self.schema: Schema = schema
        self.description = (
            self.__doc__.strip()
            if bool(self.__doc__)
            else ""
        )
        self.name: str = (
            f'"{__name}"'
            if (not bool(self.schema.name))
            else f'"{self.schema.name}"."{__name}"'
        )
        self.columns: Iterable[Column] = columns
        for (column) in self.columns:
            column.table = self
        self.constraints: Iterable[str] = constraints
        self.inherit_from: Table = inherit_from

        return None

    def __call__(self, **columns: Dict[str, Any]) -> Table:
        copy: Table = self
        copy.kwargs: Dict[str, Any] = columns
        return copy

    def create(self) -> None:
        sql: str = f'CREATE TABLE IF NOT EXISTS {self.name} ('
        columns: List[str] = []

        # If there are more than one Primary Key columns, then the
        # constraint must be set as a table constraint instead.
        primary_key_columns: List[str] = [
            column.name for (column)
            in self.columns
            if bool(column.primary_key)
        ]
        pk_is_table_constraint: bool = (len(primary_key_columns) > 1)

        for (column) in self.columns:
            if not isinstance(column, Column):
                continue
            base: str = f"{column.name} {column.data_type}"
            if (column.unique):
                base += " UNIQUE"
            if (column.not_null):
                base += " NOT NULL"
            if ((column.primary_key) and (not pk_is_table_constraint)):
                base += " PRIMARY KEY"
            if (column.reference):
                base += f" {str(column.reference)}"
                if (column.on_delete):
                    base += f" ON DELETE {column.on_delete}"
                if (column.on_update):
                    base += f" ON UPDATE {column.on_update}"
            if (column.default):
                base += f" DEFAULT {column.default}"
            if (column.check):
                base += f" CHECK ({column.check})"
            columns.append(base)

        if (pk_is_table_constraint):
            sql_primary_key: str = (
                f"PRIMARY KEY ({', '.join(primary_key_columns)})"
            )
            self.constraints.append(sql_primary_key)
            columns.append(sql_primary_key)

        sql += f"{', '.join(columns)} )"

        if (self.inherit_from):
            sql += f" INHERITS ({self.inherit_from.name})"

        return self.schema.database._execute(Statement(sql))

    def drop(self) -> None:
        return self.schema.database._execute(Statement(
            f'DROP TABLE IF EXISTS {self.name}'
        ))

    def to_model(self) -> Model:
        from .model import BaseModel, Model
        attrs: Dict[str, Any] = {
            "columns": self.columns,
            "kwargs": self.kwargs
        }
        return BaseModel(self.unaltered_name, (Model,), attrs)
