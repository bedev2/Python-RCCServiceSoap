from zeep import Client
from zeep import Transport
from zeep import Settings

from Models.response_models import *
from Models.request_models import *

# TODO: Logging like this but for PY & Configurable as it will be a part of the lib: Logger.Verbose("CloseExpiredJobs starting");

class RCCServiceSoap:
    """SOAP client for interacting with RCCService.

    Args:
        host (str): The hostname or IP address where RCCService is located.
        port (int): The port RCCService is located on.
        timeout (int): The transport timeout in seconds.
        binding_name (str): The name of the RCC binding (default is "{http://roblox.com/}RCCServiceSoap").

    Example:
        To use the client, first create an instance and call SOAP methods:
        >>> client = RCCServiceSoap('127.0.0.1', 64989, 5)
        >>> TODO: document the rest of this.
    """
    def __init__(self, host: str, port: int, timeout: int, binding_name="{http://roblox.com/}RCCServiceSoap"):
        self.host = host
        self.port = port
        self.timeout = timeout

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
        response = self.client.service.GetVersion()
        return GetVersionResponse(GetVersionResult=response)

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
        return response

    def RenewLease(self, jobId: str, expirationInSeconds: float) -> RenewLeaseResponse:
        """Calls RenewLease() on RCCService and returns a float representing the time the given Job is renewed for."""
        request = {
            'jobID': jobId,
            'expirationInSeconds': expirationInSeconds
        }

        response = self.client.service.RenewLease(**request)
        return response

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
        return response

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
        return response

    def Diag(self, type: int, jobId: str) -> str:
        # TODO
        return "todo"
    
    def GetStatus(self) -> GetStatusResponse:
        """Calls GetStatus() on RCCService and returns the response model."""
        response = self.client.service.GetStatus()
        return GetStatusResponse(GetStatusResult=response)

    def GetAllJobs(self) -> GetAllJobsExResponse:
        """Calls GetAllJobsEx() on RCCService and reutrns a response model with the array of Jobs."""
        return self.client.service.GetAllJobsEx()

    def CloseExpiredJobs(self) -> CloseExpiredJobsResponse:
        """Attempts to close all expired Jobs and returns a response model with the amount of Jobs that were closed."""
        return self.client.service.CloseExpiredJobs()
    
    def CloseAllJobs(self) -> CloseAllJobsResponse:
        """Attempts to close all Jobs and returns a response model with the amount of Jobs that were closed."""
        return self.client.service.CloseAllJobs()

    def HelloWorld(self) -> HelloWorldResponse:
        """Calls HelloWorld() on RCCService and returns the response model."""
        response = self.client.service.HelloWorld()
        return HelloWorldResponse(HelloWorldResult=response)

#endregion