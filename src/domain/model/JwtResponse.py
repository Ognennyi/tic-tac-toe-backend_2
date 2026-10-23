from dataclasses import dataclass



@dataclass
class JwtResponse:
    type: str
    access_token: str
    refresh_token: str 