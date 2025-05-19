from __future__ import annotations

from typing import TYPE_CHECKING

from .model import Model
from .statement import Statement

if TYPE_CHECKING:
    from typing import Any, Dict, List, Union

    from .core import Database
    from .table import Table


class Query:

    def __init__(self, __db: Database, /) -> None:
        self.db: Database = __db
        return None

    def fetch_one(
        self,
        __t: Union[Table, Model],
        /,
        select: List[str] = ["*"]
    ) -> None:
        from .core import FETCH_ONE
        statement: Statement = self._prepare_statement(__t, select)
        return self.db._query(statement, fetch=FETCH_ONE)

    def fetch_many(
        self,
        __t: Union[Table, Model],
        /,
        select: List[str] = ["*"]
    ) -> None:
        from .core import FETCH_MANY
        statement: Statement = self._prepare_statement(__t, select)
        return self.db._query(statement, fetch=FETCH_MANY)

    def fetch_all(
        self,
        __t: Union[Table, Model],
        /,
        select: List[str] = ["*"]
    ) -> None:
        from .core import FETCH_ALL
        statement: Statement = self._prepare_statement(__t, select)
        return self.db._query(statement, fetch=FETCH_ALL)

    def _prepare_statement(self, __t: Union[Table, Model], /, select: List[str]) -> None:
        model: Model = __t if isinstance(__t, Model) else __t.to_model()
        table_name: str = model.table.name
        placeholder: str = self.db.placeholder

        base_filter: str = ""
        values: List[str] = []

        columns: Dict[str, Any] = model.kwargs
        if (columns):
            base_filter += "WHERE "
            for (name) in columns.keys():
                value: Any = columns[name]
                base_filter += f"{name} = {placeholder} AND "
                values.append(value)

        selected_columns: str = ", ".join(select)
        sql: str = f'SELECT {selected_columns} FROM {table_name}'

        if bool(base_filter):
            sql += " " + base_filter.strip("AND ")

        return Statement(sql, tuple(values))
