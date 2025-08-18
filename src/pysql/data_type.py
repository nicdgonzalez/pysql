"""
This module implements the various data types that SQLite3 supports.
"""

from typing import NewType


def _validate_precision(precision: int, /) -> None:
    assert 0 <= precision <= 6, "precision must be between 0 and 6"


DataType = NewType("DataType", str)

BigInt = DataType("BIGINT")


def Bit(n: int, /) -> DataType:
    return DataType(f"BIT ({n})")


def VarBit(n: int, /) -> DataType:
    return DataType(f"BIT VARYING ({n})")


Boolean = DataType("BOOLEAN")


def Char(n: int, /) -> DataType:
    return DataType(f"CHARACTER ({n})")


def VarChar(n: int, /) -> DataType:
    return DataType(f"CHARACTER VARYING ({n})")


Date = DataType("DATE")
DoublePrecision = DataType("DOUBLE PRECISION")
Integer = DataType("INTEGER")


def Interval(fields: str = "", precision: int = 6) -> DataType:
    assert 0 <= precision <= 6, "precision must be between 0 and 6"
    result = "INTERVAL"

    if len(fields) > 0:
        result += f" '{fields}'"

    if precision > 0 and "SECOND" in fields:
        result += f" ({precision})"

    return DataType(result)


Numeric = DataType("NUMERIC")
Decimal = DataType("DECIMAL")
Real = DataType("REAL")
SmallInt = DataType("SMALLINT")


def Time(precision: int = 6) -> DataType:
    return DataType(f"TIME ({precision}) WITHOUT TIME ZONE")


def TimeWithTimeZone(precision: int = 6) -> DataType:
    return DataType(f"TIME ({precision}) WITH TIME ZONE")


def Timestamp(precision: int = 6) -> DataType:
    return DataType(f"TIMESTAMP ({precision}) WITHOUT TIME ZONE")


def TimestampWithTimeZone(precision: int = 6) -> DataType:
    return DataType(f"TIMESTAMP ({precision}) WITH TIME ZONE")


Xml = DataType("XML")
Json = DataType("JSON")
Bool = DataType("BOOL")
Int8 = DataType("INT8")
BigSerial = DataType("BIGSERIAL")
Serial8 = DataType("SERIAL8")
Box = DataType("BOX")
ByteA = DataType("BYTEA")
Cidr = DataType("CIDR")
Circle = DataType("CIRCLE")
Float8 = DataType("FLOAT8")
Inet = DataType("INET")
Int = DataType("INT")
Int4 = DataType("INT4")
JsonB = DataType("JSONB")
Line = DataType("LINE")
LineSegment = DataType("LSEG")
MacAddr = DataType("MACADDR")
MacAddr8 = DataType("MACADDR8")
Money = DataType("MONEY")
Path = DataType("PATH")
Point = DataType("POINT")
Polygon = DataType("POLYGON")
Float4 = DataType("FLOAT4")
Int2 = DataType("INT2")
SmallSerial = DataType("SMALLSERIAL")
Serial2 = DataType("SERIAL2")
Serial = DataType("SERIAL")
Serial4 = DataType("SERIAL4")
Text = DataType("TEXT")
TsQuery = DataType("TSQUERY")
TsVector = DataType("TSVECTOR")
TxidSnapshot = DataType("TXID_SNAPSHOT")
Uuid = DataType("UUID")
Blob = DataType("BLOB")
Null = DataType("NULL")
