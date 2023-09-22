# Copyright 2023 LA

from Models.LuaValue import LuaValue
from Models.LuaType import LuaType
from Lua import Lua

lua_val1 = LuaValue(type=LuaType.LUA_TNUMBER.value, value="69.0")
lua_val2 = LuaValue(type=LuaType.LUA_TSTRING.value, value="Hello, world!")
lua_val3 = LuaValue(type=LuaType.LUA_TBOOLEAN.value, value="true")
lua_val4 = LuaValue(type=LuaType.LUA_TNIL.value, value="")
lua_val5 = LuaValue(type=LuaType.LUA_TTABLE.value, table=[lua_val1, lua_val2, lua_val3, lua_val4])

script = Lua.NewScript("Testing", "print('Hello, world!')")
print(script.name)
print(script.script)
print(script.arguments)

empty_script = Lua.EmptyScript()
print(empty_script.name)
print(empty_script.script)
print(empty_script.arguments)

args = [lua_val1, lua_val2, lua_val3]
Lua.SetArg(args, 2, "false")
print(args)

print(Lua.ConvertLua(lua_val1))
print(Lua.ConvertLua(lua_val2))
print(Lua.ConvertLua(lua_val3))
print(Lua.ConvertLua(lua_val4))
print(Lua.ConvertLua(lua_val5))

new_args_list = Lua.new_args(69, "Hello, world!", True, None, [4, 2, 0])
for arg in new_args_list:
    print(arg.type, arg.value)

values = Lua.GetValues([lua_val1, lua_val2, lua_val3, lua_val4, lua_val5])
print(values)