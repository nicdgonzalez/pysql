from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple

__all__: List[str] = [
    "BigInt", "Bit", "VarBit", "Boolean", "Char", "VarChar", "Date",
    "DoublePrecision", "Integer", "Interval", "Numeric", "Decimal",
    "Real", "SmallInt", "Time", "TimeTZ", "Timestamp", "TimestampTZ",
    "XML", "JSON", "Bool", "Int8", "BigSerial", "Serial8", "Box",
    "ByteA", "CIDR", "Circle", "Float8", "INET", "Int", "Int4",
    "JSONB", "Line", "LineSegment", "MacAddr", "MacAddr8", "Money",
    "Path", "Point", "Polygon", "Float4", "Int2", "SmallSerial",
    "Serial2", "Serial", "Serial4", "Text", "TSQuery", "TSVector",
    "TXID_Snapshot", "UUID", "Blob", "Null", "DataType"
]


class DataType:
    """Represents a data type for columns in the database."""

    __slots__: Tuple[str, ...] = ("name")

    def __init__(self, __name: str, /) -> None:
        self.name: str = __name
        return None

    def __str__(self) -> str:
        return self.name


BigInt: DataType = DataType("BIGINT")
Bit: DataType = lambda n: DataType(f"BIT ({n})")
VarBit: DataType = lambda n: DataType(f"BIT VARYING ({n})")
Boolean: DataType = DataType("BOOLEAN")
Char: DataType = lambda n: DataType(f"CHARACTER ({n})")
VarChar: DataType = lambda n: DataType(f"CHARACTER VARYING ({n})")
Date: DataType = DataType("DATE")
DoublePrecision: DataType = DataType("DOUBLE PRECISION")
Integer: DataType = DataType("INTEGER")
Interval: DataType = lambda f="", p=6: DataType(
    f"INTERVAL"
    + (f" '{f}'" * (bool(f)))
    + (f" ({p})" * (bool(p) & ("SECOND" in f)))
)
Numeric: DataType = DataType("NUMERIC")
Decimal: DataType = DataType("DECIMAL")
Real: DataType = DataType("REAL")
SmallInt: DataType = DataType("SMALLINT")
Time: DataType = lambda p=6: DataType(f"TIME ({p}) WITHOUT TIME ZONE")
TimeTZ: DataType = lambda p=6: DataType(f"TIME ({p}) WITH TIME ZONE")
Timestamp: DataType = lambda p=6: DataType(
    f"TIMESTAMP ({p}) WITHOUT TIME ZONE"
)
TimestampTZ: DataType = lambda p=6: DataType(
    f"TIMESTAMP ({p}) WITH TIME ZONE"
)
XML: DataType = DataType("XML")
JSON: DataType = DataType("JSON")
Bool: DataType = DataType("BOOL")
Int8: DataType = DataType("INT8")
BigSerial: DataType = DataType("BIGSERIAL")
Serial8: DataType = DataType("SERIAL8")
Box: DataType = DataType("BOX")
ByteA: DataType = DataType("BYTEA")
CIDR: DataType = DataType("CIDR")
Circle: DataType = DataType("CIRCLE")
Float8: DataType = DataType("FLOAT8")
INET: DataType = DataType("INET")
Int: DataType = DataType("INT")
Int4: DataType = DataType("INT4")
JSONB: DataType = DataType("JSONB")
Line: DataType = DataType("LINE")
LineSegment: DataType = DataType("LSEG")
MacAddr: DataType = DataType("MACADDR")
MacAddr8: DataType = DataType("MACADDR8")
Money: DataType = DataType("MONEY")
Path: DataType = DataType("PATH")
Point: DataType = DataType("POINT")
Polygon: DataType = DataType("POLYGON")
Float4: DataType = DataType("FLOAT4")
Int2: DataType = DataType("INT2")
SmallSerial: DataType = DataType("SMALLSERIAL")
Serial2: DataType = DataType("SERIAL2")
Serial: DataType = DataType("SERIAL")
Serial4: DataType = DataType("SERIAL4")
Text: DataType = DataType("TEXT")
TSQuery: DataType = DataType("TSQUERY")
TSVector: DataType = DataType("TSVECTOR")
TXID_Snapshot: DataType = DataType("TXID_SNAPSHOT")
UUID: DataType = DataType("UUID")
Blob: DataType = DataType("BLOB")
Null: DataType = DataType("NULL")
