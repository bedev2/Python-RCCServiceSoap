# Copyright 2023 LA

from RCCServiceSoap import RCCServiceSoap

class GridServiceUtils:
    @staticmethod
    def GetService(address: str, port: int):
        if not address:
            return None
        
        return RCCServiceSoap(f"http://{address}:{port}")

    @staticmethod
    def GetService(address: str) -> RCCServiceSoap:
        return GridServiceUtils.GetService(address, 64989)