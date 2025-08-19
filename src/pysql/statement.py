from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from psycopg.rows import Row


class Statement(NamedTuple):
    query: str
    params: Row | None = None
