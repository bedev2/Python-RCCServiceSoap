from dataclasses import dataclass
from Models.LuaValue import LuaValue

@dataclass
class ScriptExecution:
    """Represents script execution"""
    name: str
    script: str
    arguments: list[LuaValue] = None

    def __post_init__(self):
        if self.arguments is None:
            self.arguments = []