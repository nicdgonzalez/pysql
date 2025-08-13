from __future__ import annotations

from typing import Any, Self

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
        columns: list[NamedColumn] = []

        # I considered using `filter`s and `map`s to do all this, but instead
        # decided to process each attribute one by one to retain the order
        # that the columns were defined in. I believe this behavior to be more
        # intuitive.
        for name, column in __attrs.items():
            if isinstance(column, NamedColumn):
                columns.append(column)
                continue

            if not isinstance(column, UnnamedColumn):
                continue

            columns.append(column.into_named_column(name=name))
        else:
            assert all((isinstance(c, NamedColumn) for c in columns))

        __attrs["_columns"] = columns

        return super().__new__(cls, __name, __bases, __attrs, *args, **kwargs)


class Model(metaclass=ModelMeta):
    """Represents a table from the database as a Python type.

    Raises
    ------
    EmptyTableNameError
        The keyword argument `name` in the class' subclass arguments is
        an empty string.
    InvalidColumnNameError
        All keyword arguments to this class' constructor must be valid
        column names.
    """

    _table: Table
    # Defined in `ModelMeta.__new__`. Be sure to sync any changes.
    _columns: list[NamedColumn]

    def __init_subclass__(
        cls,
        name: str | None = None,
        inherit_from: Table | None = None,
    ) -> None:
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
