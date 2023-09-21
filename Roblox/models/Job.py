from dataclasses import dataclass

@dataclass
class Job:
    """Represents a job"""
    id: str
    expirationInSeconds: float
    category: int
    cores: float