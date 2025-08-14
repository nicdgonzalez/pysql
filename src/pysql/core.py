from __future__ import annotations

import functools
from typing import TYPE_CHECKING, NamedTuple

import psycopg

if TYPE_CHECKING:
    from typing import Any

    from psycopg.rows import Row


class Statement(NamedTuple):
    query: str
    params: tuple[Any, ...] | None = None


@functools.wraps(psycopg.connect)
def connect(*args: Any, **kwargs: Any) -> Connection:
    """A thin wrapper over `psycopg.connect` that conveniently transforms
    the returned connection into our own `Connection` type.
    """
    # XXX: This probably isn't the best way to do this.
    # I didn't give it too much thought.
    kwargs.setdefault("autocommit", True)
    kwargs.setdefault("row_factory", psycopg.rows.DictRow)

    connection = psycopg.connect(*args, **kwargs)
    return Connection(connection=connection)


class Connection:
    """Represents a connection to the database."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._inner = connection

    def execute(self, statement: Statement) -> None:
        self._inner.execute(
            query=statement.query,
            params=statement.params,
            prepare=None,
            binary=False,
        )

    def fetch_one(self, statement: Statement) -> Row | None:
        return self._inner.execute(
            query=statement.query,
            params=statement.params,
            prepare=None,
            binary=False,
        ).fetchone()

    def fetch_many(self, statement: Statement, size: int = 0) -> list[Row]:
        return self._inner.execute(
            query=statement.query,
            params=statement.params,
            prepare=None,
            binary=False,
        ).fetchmany(size=size)

    def fetch_all(self, statement: Statement) -> list[Row]:
        return self._inner.execute(
            query=statement.query,
            params=statement.params,
            prepare=None,
            binary=False,
        ).fetchall()
