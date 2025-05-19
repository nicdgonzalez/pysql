from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple

__all__: List[str] = [
    "Statement"
]


class Statement:

    def __init__(
        self,
        __statement: str,
        /,
        values: Optional[Tuple[Any, ...]] = None
    ) -> None:

        self.statement: str = __statement
        self.values: Tuple[Any, ...] = values
        return None
