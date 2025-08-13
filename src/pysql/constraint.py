from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .column import NamedColumn


class ForeignKey:
    def __init__(self, column: NamedColumn) -> None:
        self.column = column

    def __str__(self) -> str:
        assert self.column.table is not None
        table = self.column.table.name
        column = self.column.name
        return f"{table} ({column})"
