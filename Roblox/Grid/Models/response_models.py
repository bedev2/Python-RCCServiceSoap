# Copyright 2023 LA

from dataclasses import dataclass

from Models.Status import Status
from Models.LuaValue import ArrayOfLuaValue
from Models.Job import ArrayOfJob

@dataclass
class HelloWorldResponse:
    """Represents the HelloWorld SOAP operation response."""
    
    HelloWorldResult: str
    """Represents the HelloWorld result; should be 'Hello World'"""

@dataclass
class GetVersionResponse:
    """Represents the GetVersion SOAP operation response."""
   
    GetVersionResult: str
    """Represents the RCCService version."""

@dataclass
class GetStatusResponse:
    """Represents the GetStatus SOAP operation response."""
    
    GetStatusResult: Status
    """Represents the status result."""

@dataclass
class OpenJobExResponse:
    """Represents the OpenJobEx SOAP operation response."""

    OpenJobExResult: ArrayOfLuaValue
    """Represents an array of all the LuaValue(s) returned."""

@dataclass
class RenewLeaseResponse:
    """Represents the RenewLease SOAP operation response."""
    
    RenewLeaseResult: float
    """Represents the Jobs new expiration"""

@dataclass
class ExecuteExResponse:
    """Represents the ExecuteEx SOAP operation response."""
    
    ExecuteExResult: ArrayOfLuaValue
    """Represents an array of all the LuaValue(s) returned."""

@dataclass
class BatchJobExResponse:
    """Represents the BatchJobEx SOAP operation response."""
    
    BatchJobExResult: ArrayOfLuaValue
    """Represents an array of all the LuaValue(s) returned."""

@dataclass
class GetExpirationResponse:
    """Represents the GetExpiratioN SOAP operation response."""
   
    GetExpirationResult: float
    """Represents the Job expiration"""

@dataclass
class GetAllJobsExResponse:
    """Represents the GetAllJobsEx SOAP operation response."""
    
    GetAllJobsExResult: ArrayOfJob
    """Represents an array of all the Jobs."""

@dataclass
class CloseExpiredJobsResponse:
    """Represents the CloseExpiredJobs() SOAP operation response."""
    
    CloseExpiredJobsResult: int
    """Represents the amount of Jobs that were closed."""

@dataclass
class CloseAllJobsResponse:
    """Represents the CloseAllJobs() SOAP operation response."""

    CloseAllJobsResult: int
    """Represents the amount of Jobs that were closed."""

@dataclass
class DiagExResponse:
    """Represents the DiagEx() SOAP operation response."""

    DiagExResult: ArrayOfLuaValue
    """Represents an array of all the LuaValue(s) returned."""