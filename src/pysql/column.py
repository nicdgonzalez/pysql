from __future__ import annotations

import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Self

    from .constraint import ForeignKey
    from .data_type import DataType
    from .table import Table


class Action(enum.StrEnum):
    NO_ACTION = "NO_ACTION"
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"


class NamedColumn:
    """Represents a column of a table in the database.

    Parameters
    ----------
    data_type
        The type that the data in this column represents.
    name
        A unique name for the column.
    unique
        Indicates the rows in this column must be one of a kind.
    not_null
        Indicates if a row is allowed to be set to `NULL`.
    primary_key
        Indicates this column contains values that uniquely identify the row.
    reference
        Links this column to a column in another table.
    on_delete
        Dictates what to do when a referenced column gets deleted.
    on_update
        Dictates what to do when a referenced column gets updated.
    default
        Set a default value for when the row is set to `NULL`.
    check
        A statement that is used to ensure values follow certain criteria.
    """

    def __init__(
        self,
        data_type: DataType,
        /,
        *,
        name: str,
        unique: bool = False,
        not_null: bool = False,
        primary_key: bool = False,
        reference: NamedColumn | ForeignKey | None = None,
        on_delete: Action = Action.NO_ACTION,
        on_update: Action = Action.NO_ACTION,
        default: Any | None = None,
        check: str | None = None,
    ) -> None:
        self.data_type = data_type
        self.name = name
        self.unique = unique
        self.not_null = not_null
        self.primary_key = primary_key
        self.reference = reference
        self.on_delete = on_delete
        self.on_update = on_update
        self.default = default
        self.check = check

        self.table: Table | None = None

    def with_table(self, table: Table) -> Self:
        self.table = table
        return self


class UnnamedColumn:
    """Represents a partial column definition of a database table. This type
    is designed for use as the value of a class attribute definition within a
    `Model` subclass.

    In this context, the column name is specified on the left-hand side of
    the assignment operator, while the column definition is defined separately
    on the right. A separate type exists for the unnamed and named variants of
    a column definition because the column's `name` attribute is required, but
    we don't want to force the user to define it at construction time. Instead,
    we define the type with missing information, and then fill in the missing
    information afterwards.

    For parameter documentation, see `NamedColumn`.
    """

    def __init__(
        self,
        data_type: DataType,
        /,
        *,
        unique: bool = False,
        not_null: bool = False,
        primary_key: bool = False,
        reference: NamedColumn | ForeignKey | None = None,
        on_delete: Action = Action.NO_ACTION,
        on_update: Action = Action.NO_ACTION,
        default: Any | None = None,
        check: str | None = None,
    ) -> None:
        self.data_type = data_type
        self.unique = unique
        self.not_null = not_null
        self.primary_key = primary_key
        self.reference = reference
        self.on_delete = on_delete
        self.on_update = on_update
        self.default = default
        self.check = check

    def into_named_column(self, name: str) -> NamedColumn:
        return NamedColumn(
            self.data_type,
            name=name,
            unique=self.unique,
            not_null=self.not_null,
            primary_key=self.primary_key,
            reference=self.reference,
            on_delete=self.on_delete,
            on_update=self.on_update,
            default=self.default,
            check=self.check,
        )


def column(
    data_type: DataType,
    /,
    *,
    name: str | None = None,
    unique: bool = False,
    not_null: bool = False,
    primary_key: bool = False,
    reference: NamedColumn | ForeignKey | None = None,
    on_delete: Action = Action.NO_ACTION,
    on_update: Action = Action.NO_ACTION,
    default: Any | None = None,
    check: str | None = None,
) -> UnnamedColumn | NamedColumn:
    """Defines the spec for a column of a table in the database.

    This function returns different types based on whether the `name` argument
    is defined or not.

    For parameter documentation, see `NamedColumn`.
    """
    if name is None:
        return UnnamedColumn(
            data_type,
            unique=unique,
            not_null=not_null,
            primary_key=primary_key,
            reference=reference,
            on_delete=on_delete,
            on_update=on_update,
            default=default,
            check=check,
        )
    else:
        return NamedColumn(
            data_type,
            name=name,
            unique=unique,
            not_null=not_null,
            primary_key=primary_key,
            reference=reference,
            on_delete=on_delete,
            on_update=on_update,
            default=default,
            check=check,
        )
