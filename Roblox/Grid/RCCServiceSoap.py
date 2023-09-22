# Copyright 2023 LA

from Helpers import _create_job_request
from Helpers import _create_script_request

import logging

from Models.Job import Job
from Models.ScriptExecution import ScriptExecution
from Models.response_models import *

from zeep import Client
from zeep import Transport
from zeep import Settings

# TODO: should we handle zeep.exceptions.Fault and make a custom exception 'SoapFault' ? 

class RCCServiceSoapClient:
    def __init__(self, host: str, port: int, timeout: int, binding_name: str = "{http://roblox.com/}RCCServiceSoap", log_level: int = logging.DEBUG):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.logger = self._configure_logger(log_level)
        self._configure_zeep()
        self.client = self._create_client(binding_name)

    def _configure_logger(self, log_level: int) -> logging.Logger:
        logging.basicConfig(level=log_level, format='[%(levelname)s] %(message)s')
        self._disable_library_loggers()
        return logging.getLogger(__name__)
    
    def _disable_library_loggers(self):
        loggers = [
            "zeep",
            "zeep.client",
            "zeep.proxy",
            "zeep.transports",
            "zeep.wsdl.wsdl",
            "zeep.wsdl.bindings.http",
            "zeep.wsdl.bindings.soap",
            "zeep.xsd.schema",
            "zeep.xsd.types.simple",
            "zeep.xsd.elements.attribute",
            "zeep.xsd.elements.element",
            "requests",
            "requests.Session"
            "urllib3",
            "urllib3.connectionpool"
        ]
        for _ in loggers:
            logging.getLogger(_).disabled = True

    def _configure_zeep(self):
        self.zeep_settings = Settings(
            strict=False, 
            force_https=False
        )
        self.transport = Transport(timeout=self.timeout, operation_timeout=self.timeout)

    def _create_client(self, binding_name: str) -> Client:
        client = Client(
            'wsdl_files/RCCService.wsdl',
            transport=self.transport,
            settings=self.zeep_settings
        )
        service_proxy = client.create_service(binding_name, f"http://{self.host}:{self.port}")
        client._default_service = service_proxy
        return client

    def GetVersion(self) -> GetVersionResponse:
        """Calls GetVersion() on RCCService and returns the response model."""
        version = None

        try:
            version = GetVersionResponse(GetVersionResult=self.client.service.GetVersion())
            self.logger.debug(f"GetVersion completed. Version = {version.GetVersionResult}")
        except Exception as ex:
            self.logger.error(f"Get version failed. Exception = {ex}")
            raise

        return version
    
    def OpenJob(self, job: Job, script: ScriptExecution) -> OpenJobExResponse:
        """Calls OpenJobEx() on RCCService and returns a response model with an array of the LuaValue(s)."""
        request = {
            **_create_job_request(job),
            **_create_script_request(script)
        }
        response = None
        self.logger.info(f"OpenJobEx starting. Job ID = {job.id}, Script name = '{script.name}'")

        try:
            response = OpenJobExResponse(OpenJobExResult=self.client.service.OpenJobEx(**request))
            self.logger.info(f"OpenJobEx completed. Job ID = {job.id}, Category = {job.category}, ExpirationInSeconds = {job.expirationInSeconds}, Script name = '{script.name}'")
        except Exception as ex:
            self.logger.error(f"OpenJobEx failed. Job ID = {job.id}, Category = {job.category}, ExpirationInSeconds = {job.expirationInSeconds}, Script name = '{script.name}', Exception = {ex}")
            raise

        return response

    def BatchJob(self, job: Job, script: ScriptExecution) -> BatchJobExResponse:
        """Calls BatchJobEx() on RCCService, similar to OpenJobEx() but this is for Jobs with a short life."""
        request = {
            **_create_job_request(job),
            **_create_script_request(script)
        }
        response = None
        self.logger.debug(f"BatchJobEx starting. Job ID = {job.id}")

        try:
            response = BatchJobExResponse(BatchJobExResult=self.client.service.BatchJobEx(**request))
            self.logger.info(f"BatchJobEx completed. Job ID = {job.id}, Category = {job.category}, ExpirationInSeconds = {job.expirationInSeconds}")
        except Exception as ex:
            self.CloseJob(job.id)
            self.logger.error(f"BatchJobEx failed. Job ID = {job.id}, Category = {job.category}, ExpirationInSeconds = {job.expirationInSeconds}, Exception = {ex}")
            raise

        return response

    def RenewLease(self, jobId: str, expirationInSeconds: float) -> RenewLeaseResponse:
        """Calls RenewLease() on RCCService and returns a float representing the time the given Job is renewed for."""
        request = {
            'jobID': jobId,
            'expirationInSeconds': expirationInSeconds
        }
        response = None
        self.logger.debug(f"RenewLease starting. Job ID = {jobId}, expirationInSeconds = {expirationInSeconds}")

        try:
            response = RenewLeaseResponse(RenewLeaseResult=self.client.service.RenewLease(**request))
            self.logger.info(f"RenewLease completed. Job ID = {jobId}, expirationInSeconds = {expirationInSeconds}")
        except Exception as ex:
            self.logger.error(f"RenewLease failed. Job ID = {jobId}, expirationInSeconds = {expirationInSeconds}, Exception = {ex}")
            raise

        return response

    def Execute(self, jobId: str, script: ScriptExecution) -> ExecuteExResponse:
        """Calls ExecuteEx() on RCCService and executes the script inside the given Job and returns a response model."""
        request = {
            'jobID': jobId,
            **_create_script_request(script)
        }
        response = None
        self.logger.debug(f"ExecuteEx starting. Job ID = {jobId}")

        try:
            response = ExecuteExResponse(ExecuteExResult=self.client.service.ExecuteEx(**request))
            self.logger.info(f"ExecuteEx completed. Job ID = {jobId}, Script name = '{script.name}'")
        except Exception as ex:
            self.logger.error(f"ExecuteEx failed. Job ID = {jobId}, Script Name = '{script.name}', exception - {ex}")
            raise

        return response

    def CloseJob(self, jobId: str) -> None:
        """Calls CloseJob() on RCCService and attempts to close the Job if it exists."""
        # TODO: Arbiter.cs#L186
        request = {
            'jobID': jobId
        }
        self.logger.debug(f"CloseJob starting. Job ID = {jobId}")

        try:
            self.client.service.CloseJob(**request)
            self.logger.info(f"CloseJob completed. Job ID = {jobId}")
        except Exception as ex:
            self.logger.error(f"CloseJob failed. Exception = {ex}")

    def GetExpiration(self, jobId: str) -> GetExpirationResponse:
        """Calls GetExpiration() on RCCService and returns a float representing the seconds until Job is expired."""
        request = {
            'jobID': jobId
        }
        self.logger.debug(f"GetExpiration. Job ID = {jobId}")

        response = GetExpirationResponse(GetExpirationResult=self.client.service.GetExpiration(**request))
        return response

    def Diag(self, type: int, jobId: str) -> DiagExResponse:
        request = {
            'type': type,
            'jobID': jobId
        }
        response = None
        self.logger.debug(f"DiagEx. Type = {type}, Job ID = {jobId}")

        try:
            response = DiagExResponse(DiagExResult=self.client.service.DiagEx(**request))
        except Exception as ex:
            self.logger.error(f"DiagEx failed. Job ID = {jobId}, exception = {ex}")
            raise

        return response
    
    def GetStatus(self) -> GetStatusResponse:
        """Calls GetStatus() on RCCService and returns the response model."""
        self.logger.debug("GetStatus starting")
        response = GetStatusResponse(GetStatusResult=self.client.service.GetStatus())
        self.logger.debug(f"GetStatus completed. EnvironmentCount = {response.GetStatusResult.environmentCount}, version = {response.GetStatusResult.version}")
        
        return response

    def GetAllJobs(self) -> GetAllJobsExResponse:
        """Calls GetAllJobsEx() on RCCService and reutrns a response model with the array of Jobs."""
        self.logger.debug("GetAllJobsEx starting")
        response = GetAllJobsExResponse(GetAllJobsExResult=self.client.service.GetAllJobsEx())
        self.logger.debug(f"GetAllJobsEx completed. Job count = {response.GetAllJobsExResult.Job.count}")

        return response

    def CloseExpiredJobs(self) -> CloseExpiredJobsResponse:
        """Attempts to close all expired Jobs and returns a response model with the amount of Jobs that were closed."""
        self.logger.debug("CloseExpiredJobs starting")
        response = CloseExpiredJobsResponse(CloseExpiredJobsResult=self.client.service.CloseExpiredJobs())
        self.logger.debug(f"CloseExpiredJobs completed. Result = {response.CloseExpiredJobsResult}")
        
        return response
    
    def CloseAllJobs(self) -> CloseAllJobsResponse:
        """Attempts to close all Jobs and returns a response model with the amount of Jobs that were closed."""
        self.logger.debug("CloseAllJobs starting")
        response = CloseAllJobsResponse(CloseAllJobsResult=self.client.service.CloseAllJobs())
        self.logger.debug(f"CloseAllJobs completed. Result = {response.CloseAllJobsResult}")

        return response

    def HelloWorld(self) -> HelloWorldResponse:
        """Calls HelloWorld() on RCCService and returns the response model."""
        response = self.client.service.HelloWorld()
        return HelloWorldResponse(HelloWorldResult=response)