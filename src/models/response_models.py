from dataclasses import dataclass

@dataclass
class HelloWorldResponse:
    """Represents the HelloWorld SOAP operation response."""
    HelloWorldResult: str