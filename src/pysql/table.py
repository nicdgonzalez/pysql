from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .column import NamedColumn


class Table:
    def __init__(self, name: str, columns: list[NamedColumn]) -> None:
        self._name = name
        self._columns = columns
        self._column_names = set((c.name for c in self._columns))

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> list[NamedColumn]:
        return self._columns

    @property
    def column_names(self) -> set[str]:
        return self._column_names

    def is_valid_column(self, name: str) -> bool:
        return name in self._column_names
