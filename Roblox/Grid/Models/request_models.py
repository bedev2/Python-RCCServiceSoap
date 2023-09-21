from dataclasses import dataclass
from Models.Job import Job
from Models.ScriptExecution import ScriptExecution

@dataclass
class OpenJobExRequest:
    """Represents a request model for OpenJob SOAP operation."""
    job: Job
    script: ScriptExecution