from __future__ import annotations

from typing import TYPE_CHECKING

from .column import Column
from .table import Table

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Type, Union


class BaseModel(type):

    def __new__(
        cls: Type[BaseModel],
        __name: str,
        __bases: Tuple[type, ...],
        __attrs: Dict[str, Any],
        /,
        **kwargs: Dict[str, Any]
    ) -> type@__new__:
        columns: List[Column] = []
        for (name, column) in __attrs.items():
            if not isinstance(column, Column):
                continue
            column.name = name
            columns.append(column)
        __attrs["columns"] = columns
        return super().__new__(cls, __name, __bases, __attrs, **kwargs)


class Model(metaclass=BaseModel):

    def __init_subclass__(
        cls: Type[Model],
        name: Optional[str] = None,
        inherit_from: Optional[Union[Table, Model]] = None
    ) -> None:
        table_name: str = name if bool(name) else cls.__name__
        cls.table: Table = Table(
            table_name,
            schema=cls.db.schema,
            columns=cls.columns,
            inherit_from=inherit_from
        )
        cls.table.description = (
            cls.__doc__.strip()
            if bool(cls.__doc__)
            else ""
        )
        cls.table.schema.tables.append(cls)
        return None

    def __new__(cls, **columns) -> Table:
        return cls.table(**columns)
