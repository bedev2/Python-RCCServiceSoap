from dataclasses import dataclass
from models.Job import Job
from models.ScriptExecution import ScriptExecution

@dataclass
class OpenJobExRequest:
    """Represents a request model for OpenJob SOAP operation."""
    job: Job
    script: ScriptExecution