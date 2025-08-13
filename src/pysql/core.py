from __future__ import annotations

import functools
from typing import TYPE_CHECKING

import psycopg

if TYPE_CHECKING:
    from typing import Any


@functools.wraps(psycopg.connect)
def connect(*args: Any, **kwargs: Any) -> Connection:
    """A wrapper over :func:`psycopg.connect` that conveniently transforms
    the returned connection into our own :class:`Connection` type.
    """
    connection = psycopg.connect(*args, **kwargs)
    return Connection(connection=connection)


class Connection:
    """Represents a connection to the database."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._inner = connection
