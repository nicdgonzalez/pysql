from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

    from .column import Column

__all__: List[str] = [
    'ForeignKey'
]


class ForeignKey:

    def __init__(self, column: Column, /) -> None:
        self.column: Column = column
        return None

    def __str__(self) -> str:
        return f'REFERENCES {self.column.table.name} ({self.column.name})'


#
