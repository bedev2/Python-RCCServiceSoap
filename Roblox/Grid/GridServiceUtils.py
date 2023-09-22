# Copyright 2023 LA

from RCCServiceSoap import RCCServiceSoapClient

class GridServiceUtils:
    @staticmethod
    def GetService(address: str, port: int, timeout: int = 20):
        if not address:
            return None
        
        return RCCServiceSoapClient(address, port, timeout)