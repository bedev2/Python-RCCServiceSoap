from zeep import Client
from zeep import Transport
from zeep import Settings

from Models.response_models import *
from Models.request_models import *

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

    def HelloWorld(self) -> HelloWorldResponse:
        """Calls HelloWorld() on RCCService and returns the response model."""
        response = self.client.service.HelloWorld()
        return HelloWorldResponse(HelloWorldResult=response)
    
    def GetVersion(self) -> GetVersionResponse:
        """Calls GetVersion() on RCCService and returns the response model."""
        response = self.client.service.GetVersion()
        return GetVersionResponse(GetVersionResult=response)
    
    def GetStatus(self) -> GetStatusResponse:
        """Calls GetStatus() on RCCService and returns the response model."""
        response = self.client.service.GetStatus()
        return GetStatusResponse(GetStatusResult=response)
    
    # terrible, thank you zeep and python
    def OpenJobEx(self, job: Job, script: ScriptExecution) -> OpenJobExResponse:
        """Calls OpenJobEx() on RCCService and returns the response model."""
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