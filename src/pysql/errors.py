class PysqlException(Exception):
    pass


class EmptyTableNameError(PysqlException):
    def __init__(self, *_args: object) -> None:
        super().__init__("expected table name to not be empty")


class InvalidColumnNameError(PysqlException):
    def __init__(
        self,
        column_name: str,
        table_name: str,
        *_args: object,
    ) -> None:
        super().__init__(f"no column named {column_name!r} in {table_name!r}")
