from dataclasses import dataclass
from Models.LuaType import LuaType

@dataclass
class LuaValue:
    """Represents a LuaValue"""
    type: LuaType = LuaType.LUA_TNIL
    value: str = ""
    table: list["LuaValue"] = None

@dataclass
class ArrayOfLuaValue:
    LuaValue: list[LuaValue]