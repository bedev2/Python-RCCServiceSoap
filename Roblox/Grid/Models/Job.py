# Copyright 2023 LA

from dataclasses import dataclass

@dataclass
class Job:
    """Represents a job"""
    id: str
    expirationInSeconds: float
    category: int
    cores: float

@dataclass
class ArrayOfJob:
    """Represents an array of the Job class"""
    Job: list[Job]