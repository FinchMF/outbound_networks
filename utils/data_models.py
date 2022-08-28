from dataclasses import dataclass


@dataclass
class Endpoint_Record:

    endpoint: str
    outbounds: str
    count: int