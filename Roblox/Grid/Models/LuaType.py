# Copyright 2023 LA

from enum import Enum

class LuaType(Enum):
    LUA_TNIL = "LUA_TNIL"
    LUA_TBOOLEAN = "LUA_TBOOLEAN"
    LUA_TNUMBER = "LUA_TNUMBER"
    LUA_TSTRING = "LUA_TSTRING"
    LUA_TTABLE = "LUA_TTABLE"