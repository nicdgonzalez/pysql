from __future__ import annotations

from typing import Any

from .column import NamedColumn, UnnamedColumn
from .errors import EmptyTableNameError, InvalidColumnNameError
from .table import Table


class ModelMeta(type):
    _columns: list[NamedColumn]

    def __new__(
        cls,
        __name: str,
        __bases: tuple[type, ...],
        __attrs: dict[str, Any],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> ModelMeta:
        self = super().__new__(cls, __name, __bases, __attrs, *args, **kwargs)
        self._columns = []

        for name, column in __attrs.items():
            if isinstance(column, NamedColumn):
                self._columns.append(column)
                continue

            if not isinstance(column, UnnamedColumn):
                continue

            self._columns.append(column.into_named_column(name=name))
        else:
            assert all((isinstance(c, NamedColumn) for c in self._columns))

        return self


class Model(metaclass=ModelMeta):
    """Represents a table from the database as a Python type.

    Raises
    ------
    EmptyTableNameError
        Attempted to override the table name with an empty string.
    InvalidColumnNameError
        An invalid keyword argument was passed to the constructor.
    """

    _table: Table
    _columns: list[NamedColumn]  # Defined in `ModelMeta.__new__`.

    def __init_subclass__(
        cls,
        name: str | None = None,
        inherit_from: Table | None = None,
    ) -> None:
        # TODO: Convert CamelCase into snake_case properly.
        table_name = name if name is not None else cls.__name__.lower()

        if len(table_name) < 1:
            raise EmptyTableNameError()

        cls._table = Table(name=table_name, columns=cls._columns)

    def __init__(self, **record: Any) -> None:
        for column_name in record.keys():
            if column_name not in self._table.column_names:
                raise InvalidColumnNameError(
                    column_name=column_name,
                    table_name=self._table.name,
                )

        self.record: dict[str, Any] = record

    @property
    def table(self) -> Table:
        return self._table

