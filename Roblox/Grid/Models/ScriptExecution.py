# Copyright 2023 LA

from dataclasses import dataclass, field
from Models.LuaValue import LuaValue

@dataclass
class ScriptExecution:
    """Represents script execution"""
    name: str
    script: str
    arguments: list[LuaValue] = field(default_factory=list)