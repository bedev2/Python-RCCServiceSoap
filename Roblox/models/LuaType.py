from enum import Enum

class LuaType(Enum):
    LUA_TNIL = 1
    LUA_TBOOLEAN = 2
    LUA_TNUMBER = 3
    LUA_TSTRING = 4
    LUA_TTABLE = 5