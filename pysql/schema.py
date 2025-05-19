from __future__ import annotations

from typing import TYPE_CHECKING

from .errors import MissingSchemaNameError
from .statement import Statement

if TYPE_CHECKING:
    from typing import List, Optional

    from .core import Database
    from .table import Table

__all__: List[str] = [
    "Schema"
]


class Schema:
    """Represents a schema in the database."""

    def __init__(
        self,
        __db: Database,
        /,
        owner: Optional[str],
        name: Optional[str] = None
    ) -> None:
        self.database: Database = __db
        self.owner: str = owner
        self.name: str = name if name else owner
        self.tables: List[Table] = []
        return self.database.schemas.append(self)

    def create(self) -> None:
        if (not self.name):
            raise MissingSchemaNameError(
                "Unable to create a schema with no owner or name."
            )

        return self.database._execute(Statement(
            "CREATE SCHEMA "
            + (f'"{self.name}" ' * bool(self.name))
            + (f'"{self.owner}" ' * (not bool(self.name)))
            + (f'AUTHORIZATION "{self.owner}"')
        ))

    def drop(self, force: bool = False) -> None:
        if (not self.name):
            raise MissingSchemaNameError(
                "Unable to drop a schema with no owner or name."
            )

        return self.database._execute(Statement(
            (f'DROP SCHEMA "{self.name}"')
            + ("CASCADE" * (force))
        ))
