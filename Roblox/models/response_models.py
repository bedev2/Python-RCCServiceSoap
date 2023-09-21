from dataclasses import dataclass

from models.Status import Status
from models.LuaValue import ArrayOfLuaValue

@dataclass
class HelloWorldResponse:
    """Represents the HelloWorld SOAP operation response."""
    HelloWorldResult: str

@dataclass
class GetVersionResponse:
    """Represents the GetVersion SOAP operation response."""
    GetVersionResult: str

@dataclass
class GetStatusResponse:
    """Represents the GetStatus SOAP operation response."""
    GetStatusResult: Status

@dataclass
class OpenJobExResponse:
    """Represents the OpenJobEx SOAP operation response."""
    OpenJobExResult: ArrayOfLuaValue