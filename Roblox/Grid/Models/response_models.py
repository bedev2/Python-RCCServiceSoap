from dataclasses import dataclass

from Models.Status import Status
from Models.LuaValue import ArrayOfLuaValue
from Models.Job import ArrayOfJob

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

@dataclass
class RenewLeaseResponse:
    """Represents the RenewLease SOAP operation response."""
    RenewLeaseResult: float

@dataclass
class ExecuteExResponse:
    """Represents the ExecuteEx SOAP operation response."""
    ExecuteExResult: ArrayOfLuaValue

@dataclass
class BatchJobExResponse:
    """Represents the BatchJobEx SOAP operation response."""
    BatchJobExResult: ArrayOfLuaValue

@dataclass
class GetExpirationResponse:
    """Represents the GetExpiratioN SOAP operation response."""
    GetExpirationResult: float

@dataclass
class GetAllJobsExResponse:
    """Represents the GetAllJobsEx SOAP operation response."""
    GetAllJobsExResult: ArrayOfJob