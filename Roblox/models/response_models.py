from dataclasses import dataclass

@dataclass
class HelloWorldResponse:
    """Represents the HelloWorld SOAP operation response."""
    HelloWorldResult: str

@dataclass
class GetVersionResponse:
    """Represents the GetVersion SOAP operation response."""
    GetVersionResult: str

@dataclass
class Status:
    version: str
    environmentCount: int

@dataclass
class GetStatusResponse:
    """Represents the GetStatus SOAP operation response."""
    GetStatusResult: Status