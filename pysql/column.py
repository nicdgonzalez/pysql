from __future__ import annotations

from typing import TYPE_CHECKING

from .constraints import ForeignKey
from .statement import Statement
from .types import DataType

if TYPE_CHECKING:
    from typing import Any, List, Optional, Union

    from .table import Table

__all__: List[str] = [
    "NO_ACTION",
    "CASCADE",
    "RESTRICT",
    "Column"
]


NO_ACTION: str = "NO_ACTION"
CASCADE: str = "CASCADE"
RESTRICT: str = "RESTRICT"


class Column:
    """Represents a table column in the database."""

    table: Table  # The table this column belongs to.

    def __init__(
        self,
        __name: Optional[str] = None,
        __data_type: Optional[DataType] = None,
        /,
        *,
        name: str = None,
        data_type: DataType = None,
        unique: bool = False,
        not_null: bool = False,
        primary_key: bool = False,
        reference: Optional[Union[Column, ForeignKey]] = None,
        on_delete: Optional[str] = None,
        on_update: Optional[str] = None,
        default: Optional[Any] = None,
        check: Optional[str] = None
    ) -> None:

        pos_args: List[Union[str, DataType]] = [
            arg for arg
            in (__name, __data_type)
            if (arg is not None)
        ]

        error: str = "'%s' is defined in positional AND keyword argument."
        if (pos_args):
            if (isinstance(pos_args[0], str)):
                if (name):
                    raise Exception(error % ("name"))
                name = pos_args.pop(0)
            elif (isinstance(pos_args[0], DataType)):
                if (data_type):
                    raise Exception(error % ("data_type"))
                data_type = pos_args.pop(0)

        if (pos_args):
            if (isinstance(pos_args[0], DataType)):
                if (data_type):
                    raise Exception(error % ("data_type"))
                data_type = pos_args.pop(0)

        if ((reference) and (not isinstance(reference, ForeignKey))):
            if isinstance(reference, Column):
                reference = ForeignKey(reference)
            else:
                error *= 0
                error += "Parameter '%s' must be of type :class:`%s`."
                raise TypeError(error % ("reference", "ForeignKey"))

        self.name: str = name
        self.data_type: DataType = data_type
        self.unique: bool = unique
        self.not_null: bool = not_null
        self.primary_key: bool = primary_key
        self.reference: ForeignKey = reference
        self.on_delete: str = on_delete
        self.on_update: str = on_update
        self.default: Any = (
            f"'{default}'"
            if isinstance(default, str)
            else default
        )
        self.check: str = check

        return None

    def rename(self, new_name: str) -> Statement:
        assert(bool(self.name)), "Column with no name can not be renamed."
        self.name = new_name
        return self.table.schema.database._execute(Statement(
            f'ALTER TABLE IF EXISTS {self.table.name} '
            f'RENAME COLUMN "{self.name}" TO "{new_name}"'
        ))
