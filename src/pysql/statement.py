from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing import Any


class Statement(NamedTuple):
    query: str
    params: tuple[Any, ...] | None = None
