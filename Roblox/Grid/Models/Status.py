# Copyright 2023 LA

from dataclasses import dataclass

@dataclass
class Status:
    version: str
    environmentCount: int