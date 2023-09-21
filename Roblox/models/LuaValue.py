from dataclasses import dataclass
from models.LuaType import LuaType

@dataclass
class LuaValue:
    """Represents a LuaValue"""
    type: LuaType
    value: str
    table: list["LuaValue"]

@dataclass
class ArrayOfLuaValue:
    LuaValue: list[LuaValue]