# Copyright 2023 LA

import logging

from Models.Job import Job
from Models.ScriptExecution import ScriptExecution
from Models.response_models import *

from zeep import Client
from zeep import Transport
from zeep import Settings

# TODO: Logging like this but for PY & Configurable as it will be a part of the lib: Logger.Verbose("CloseExpiredJobs starting");

class RCCServiceSoap:
    """SOAP client for interacting with RCCService.

    Args:
        host (str): The hostname or IP address where RCCService is located.
        port (int): The port RCCService is located on.
        timeout (int): The transport timeout in seconds.
        binding_name (str): The name of the RCC binding (default is "{http://roblox.com/}RCCServiceSoap").
        log_level (int): The level the logger will use, see https://docs.python.org/3/library/logging.html#levels for levels.

    Example:
        To use the client, first create an instance and call SOAP methods:
        >>> client = RCCServiceSoap('127.0.0.1', 64989, 5)
        >>> TODO: document the rest of this.
    """
    def __init__(self, host: str, port: int, timeout: int, binding_name: str = "{http://roblox.com/}RCCServiceSoap", log_level: int = logging.DEBUG):
        self.host = host
        self.port = port
        self.timeout = timeout

        # Configure logger
        logging.basicConfig(level=log_level, format='[%(levelname)s] %(message)s')
        self.logger = logging.getLogger(__name__)

        # Configure zeep
        zeep_settings = Settings(
            strict=False, 
            force_https=False
        )

        # Create client
        self.transport = Transport(timeout=timeout, operation_timeout=timeout)
        self.client = Client(
            'wsdl_files/RCCService.wsdl',
            transport=self.transport,
            settings=zeep_settings
        )

        service_proxy = self.client.create_service(binding_name=binding_name, address=f"http://{host}:{port}")
        self.client._default_service = service_proxy

#region Operations

    def GetVersion(self) -> GetVersionResponse:
        """Calls GetVersion() on RCCService and returns the response model."""
        version = None

        try:
            version = self.client.service.GetVersion()
            self.logger.debug(f"GetVersion completed. Version = {version}")
        except Exception as ex:
            self.logger.error(f"Get version failed. Exception = {ex}")
            raise

        return GetVersionResponse(GetVersionResult=version)

    def OpenJob(self, job: Job, script: ScriptExecution) -> OpenJobExResponse:
        """Calls OpenJobEx() on RCCService and returns a response model with an array of the LuaValue(s)."""
        request = {
            'job': {
                'id': job.id,
                'expirationInSeconds': job.expirationInSeconds,
                'category': job.category,
                'cores': job.cores
            },
            'script': {
                'name': script.name,
                'script': script.script,
                'arguments': {
                    'LuaValue': script.arguments
                }
            }
        }

        response = self.client.service.OpenJobEx(**request)
        return OpenJobExResponse(OpenJobExResult=response)

    def BatchJob(self, job: Job, script: ScriptExecution) -> BatchJobExResponse:
        """Calls BatchJobEx() on RCCService, similar to OpenJobEx() but this is for Jobs with a short life."""
        # TODO: Taken from OpenJobEx(), we can probably reduce boilerplate for reqs
        request = {
            'job': {
                'id': job.id,
                'expirationInSeconds': job.expirationInSeconds,
                'category': job.category,
                'cores': job.cores
            },
            'script': {
                'name': script.name,
                'script': script.script,
                'arguments': {
                    'LuaValue': script.arguments
                }
            }
        }

        response = self.client.service.BatchJobEx(**request)
        return BatchJobExResponse(BatchJobExResult=response)

    def RenewLease(self, jobId: str, expirationInSeconds: float) -> RenewLeaseResponse:
        """Calls RenewLease() on RCCService and returns a float representing the time the given Job is renewed for."""
        request = {
            'jobID': jobId,
            'expirationInSeconds': expirationInSeconds
        }

        response = self.client.service.RenewLease(**request)
        return RenewLeaseResponse(RenewLeaseResult=response)

    def Execute(self, jobId: str, script: ScriptExecution) -> ExecuteExResponse:
        """Calls ExecuteEx() on RCCService and executes the script inside the given Job and returns a response model."""
        request = {
            'JobID': jobId,
            'script': {
                'name': script.name,
                'script': script.script,
                'arguments': {
                    'LuaValue': script.arguments
                }
            }
        }

        response = self.client.service.ExecuteEx(**request)
        return ExecuteExResponse(ExecuteExResult=response)

    def CloseJob(self, jobId: str) -> None:
        """Calls CloseJob() on RCCService and attempts to close the Job if it exists."""
        # TODO: Arbiter.cs#L186
        request = {
            'JobID': jobId
        }

        self.client.service.CloseJob(**request)

    def GetExpiration(self, jobId: str) -> GetExpirationResponse:
        """Calls GetExpiration() on RCCService and returns a float representing the seconds until Job is expired."""
        request = {
            'JobID': jobId
        }

        response = self.client.service.GetExpiration(**request)
        return GetExpirationResponse(GetExpirationResult=response)

    def Diag(self, type: int, jobId: str) -> DiagExResponse:
        request = {
            'type': type,
            'JobID': jobId
        }

        response = self.client.service.DiagEx(**request)
        return DiagExResponse(DiagExResult=response)
    
    def GetStatus(self) -> GetStatusResponse:
        """Calls GetStatus() on RCCService and returns the response model."""
        response = self.client.service.GetStatus()
        return GetStatusResponse(GetStatusResult=response)

    def GetAllJobs(self) -> GetAllJobsExResponse:
        """Calls GetAllJobsEx() on RCCService and reutrns a response model with the array of Jobs."""
        return GetAllJobsExResponse(GetAllJobsExResult=self.client.service.GetAllJobsEx())

    def CloseExpiredJobs(self) -> CloseExpiredJobsResponse:
        """Attempts to close all expired Jobs and returns a response model with the amount of Jobs that were closed."""
        return CloseExpiredJobsResponse(CloseExpiredJobsResult=self.client.service.CloseExpiredJobs())
    
    def CloseAllJobs(self) -> CloseAllJobsResponse:
        """Attempts to close all Jobs and returns a response model with the amount of Jobs that were closed."""
        return CloseAllJobsResponse(CloseAllJobsResult=self.client.service.CloseAllJobs())

    def HelloWorld(self) -> HelloWorldResponse:
        """Calls HelloWorld() on RCCService and returns the response model."""
        response = self.client.service.HelloWorld()
        return HelloWorldResponse(HelloWorldResult=response)

#endregion