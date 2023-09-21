from zeep import Client
from zeep import Transport
from zeep import Settings

from models.response_models import *

class RCCServiceSoap:
    """SOAP client for interacting with RCCService.

    Args:
        host (str): The hostname or IP address where RCCService is located.
        port (int): The port RCCService is located on.
        timeout (int): The transport timeout in seconds.

    Example:
        To use the client, first create an instance and call SOAP methods:
        >>> client = RCCServiceSoap('127.0.0.1', 64989, 5)
        >>> TODO: document the rest of this.
    """
    def __init__(self, host: str, port: int, timeout: int):
        self.host = host
        self.port = port
        self.timeout = timeout

        zeep_settings = Settings(strict=False, force_https=False)

        self.transport = Transport(timeout=timeout, operation_timeout=timeout)
        self.client = Client(
            'wsdl_files/RCCService.wsdl',
            transport=self.transport,
            settings=zeep_settings
        )

        # https://github.com/mvantellingen/python-zeep/issues/833, this is kinda bad because some people may patch or change their RCC binding name to something else but usually its left as roblox.com
        # TODO: add arg for binding name ?
        service_proxy = self.client.create_service(binding_name="{http://roblox.com/}RCCServiceSoap", address=f"http://{host}:{port}")
        self.client._default_service = service_proxy

    def HelloWorld(self) -> HelloWorldResponse:
        """Calls HelloWorld on the RCCService instance and returns the response model."""
        response = self.client.service.HelloWorld()
        return HelloWorldResponse(HelloWorldResult=response)