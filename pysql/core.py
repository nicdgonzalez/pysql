from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING
from urllib.parse import quote as uri_quote

from .model import Model
from .query import Query
from .schema import Schema
from .session import Session
from .statement import Statement

if TYPE_CHECKING:
    from logging import Logger
    from typing import Any, Dict, List, Optional, Tuple


__all__: List[str] = [
    "FETCH_ONE",
    "FETCH_MANY",
    "FETCH_ALL",
    "DatabaseURI",
    "Database"
]

FETCH_ONE: int = 0
FETCH_MANY: int = 1
FETCH_ALL: int = 2

_log: Logger = getLogger(__name__)


class DatabaseURI:
    """Stores the components of a database connection string."""

    def __init__(
        self,
        engine: str,
        user: Optional[str] = "",
        password: Optional[str] = "",
        host: Optional[str] = "",
        port: Optional[str] = "",
        database: Optional[str] = "",
        **params: Optional[Dict[str, Any]]
    ) -> None:
        """Constructor for new `DatabaseURI` objects.

        Parameters
        -----------
        engine: :class:`str`
            The schema identifier. This is the part of the connection
            string prepending the first `://` (e.g., 'postgres').
        user: Optional[:class:`str`]
            An optional username for the database client.
        password: Optional[:class:`str`]
            An optional password to authenticate the user.
        host: Optional[:class:`str`]
            An optional IP address, DNS name, or locally resolvable
            name of a server to connect to.
        port: Optional[:class:`str`]
            Indicates which port the host is listening to. This option
            is optional if the database engine provides a default port.
        database: Optional[:class:`str`]
            An optional name of a database to connect to.
        params: Optional[:class:`str`]
            Any additional options to use when connecting. Refer to
            the database engine's documentation for available options.

        Returns ``None``.
        """

        self.engine: str = engine
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: str = port
        self.database: str = database
        self.params: dict = params

        return None

    def __str__(self) -> str:
        return self.uri

    @property
    def uri(self) -> str:
        uri_base: str = self.engine + "://"

        uri_base += (
            f"{self.user}"
            * (bool(self.user) & bool(self.host))
        )
        uri_base += (
            f":{uri_quote(self.password)}"
            * (bool(self.user) & bool(self.password))
        )
        uri_base += (
            f"@{self.host}"
            * bool(self.host)
        )
        uri_base += (
            f":{self.port}"
            * (bool(self.host) & bool(self.port))
        )
        uri_base += (
            f"/{self.database}"
            * (bool(self.database) & bool(self.host))
            # For SQLite3 connections that don't use a host.
            + self.database
            * (bool(self.database) & (not bool(self.host)))
        )

        uri_base += ("?" * bool(self.params)) + "&".join([
            f"{k}={uri_quote(v) if isinstance(v, str) else v}" for (k, v)
            in self.params.items()
        ]) * bool(self.params)

        return uri_base


class Database:
    """Represents a database connection."""

    schemas: List[Schema] = []
    placeholder: str = "%s"

    def __init__(
        self,
        __connect: Any,
        /,
        schema_name: Optional[str] = None,
        **connect_kwargs
    ) -> None:

        self.schema: Schema = Schema(self, schema_name)
        self.connection: Any = __connect(**connect_kwargs)

        self.Model: Model = Model
        self.session: Session = Session(self)
        self.query: Query = Query(self)

        self.schema.database = self
        self.Model.db = self

        return None

    def _execute(self, __s: Statement, /) -> None:
        _log.info((__s.statement, __s.values))
        c: Any = self.connection.cursor()
        (
            c.execute(__s.statement)
            if (not __s.values)
            else c.execute(__s.statement, __s.values)
        )
        self.connection.commit()
        return None

    def _query(self, __s: Statement, /, *, fetch: int = FETCH_ONE) -> Any:
        _log.info((__s.statement, __s.values))

        c: Any = self.connection.cursor()
        fetch_options: Tuple[Any, ...] = (c.fetchone, c.fetchmany, c.fetchall)
        (
            c.execute(__s.statement)
            if (not __s.values)
            else c.execute(__s.statement, __s.values)
        )
        return fetch_options[fetch]()
