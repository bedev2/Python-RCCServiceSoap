from dataclasses import dataclass
from models.LuaValue import LuaValue
from typing import List

@dataclass
class ScriptExecution:
    """Represents script execution"""
    name: str
    script: str
    arguments: List[LuaValue] = None

    def __post_init__(self):
        if self.arguments is None:
            self.arguments = []