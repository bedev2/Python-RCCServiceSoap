# Copyright 2023 LA

from Models.ScriptExecution import ScriptExecution
from Models.LuaValue import LuaValue
from Models.LuaType import LuaType

class Lua:
    """Provides utility methods for working with Lua scripts."""

    @staticmethod
    def NewScript(name: str, script: str, args: list[LuaValue] = None) -> ScriptExecution:
        """
        Creates a new script.

        Args:
            name (str): The name of the script.
            script (str): The full script.
            args (list[LuaValue]): The arguments to pass to the script.
        """
        if args is None:
            args = []

        return ScriptExecution(name=name, script=script, arguments=args)

    @staticmethod
    def EmptyScript() -> ScriptExecution:
        return Lua.NewScript("EmptyScript", "return")

    @staticmethod
    def SetArg(args: list[LuaValue], index: int, value) -> None:
        lua_value = LuaValue()

        if isinstance(value, (int, float)):
            lua_value.type = LuaType.LUA_TNUMBER.value
            lua_value.value = str(value)
        elif isinstance(value, str):
            lua_value.type = LuaType.LUA_TSTRING.value
            lua_value.value = str(value)
        elif isinstance(value, bool):
            lua_value.type = LuaType.LUA_TBOOLEAN.value
            lua_value.value = "true" if value else "false" # maybe this could just be str(value) but i wanna make it 1:1 to the C# or as similar as possible.
        elif value is None:
            lua_value.type = LuaType.LUA_TNIL.value
            lua_value.value = ""
        elif isinstance(value, list):
            lua_value.type = LuaType.LUA_TTABLE.value
            lua_value.table = value
        else:
            raise ValueError(f"Unsupported Lua argument type {type(value)}, value = '{value}'")

        args[index] = lua_value

    @staticmethod
    def ConvertLua(lua_value: LuaValue) -> any:
        """
        Converts a LuaValue to the Python equivalent.

        Args:
            lua_value (LuaValue): The LuaValue.
        """        
        if lua_value.type == LuaType.LUA_TBOOLEAN.value:
            return bool(lua_value.value.lower() == "true")
        elif lua_value.type == LuaType.LUA_TNUMBER.value:
            return float(lua_value.value)
        elif lua_value.type == LuaType.LUA_TSTRING.value:
            return lua_value.value
        elif lua_value.type == LuaType.LUA_TTABLE.value:
            return Lua.GetValues(lua_value.table)
        else:
            return None

    def new_args(*args) -> list[LuaValue]:
        """
        Converts a list of args into a list of LuaValue(s).

        Args:
            *args: The arguments to convert.

        Returns:
            List[LuaValue]: A list of LuaValue objects.
        """
        lua_args = []

        for arg in args:
            # empty lua value
            lua_value = LuaValue(type=None, value="")

            if arg is None:
                lua_value.type = LuaType.LUA_TNIL
            elif isinstance(arg, bool):
                lua_value.type = LuaType.LUA_TBOOLEAN
                lua_value.value = str(arg)
            elif isinstance(arg, (int, float)):
                lua_value.type = LuaType.LUA_TNUMBER
                lua_value.value = str(arg)
            elif isinstance(arg, str):
                lua_value.type = LuaType.LUA_TSTRING
                lua_value.value = arg
            elif isinstance(arg, list):
                lua_value.type = LuaType.LUA_TTABLE
                lua_value.table = [LuaValue(type=None, value="", table=item) for item in arg]
            else:
                raise ValueError(f"Unsupported Lua argument type {type(arg)}, value = '{arg}'")
            
            # add to the lua_args array
            lua_args.append(lua_value)

        return lua_args

    @staticmethod
    def GetValues(args: list[LuaValue]) -> list[any]:
        values = []

        for lua_value in args:
            values.append(Lua.ConvertLua(lua_value))
        
        return values