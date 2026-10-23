from abc import ABC, abstractmethod
from domain.model.sign_up_request import SignUpRequest

from domain.model.JwtRequest import JwtRequest
from domain.model.JwtResponse import JwtResponse
from domain.model.RefreshJwtRequest import RefreshJwtRequest

class AuthService(ABC):

    @abstractmethod
    def sign_up(self, request: SignUpRequest) -> bool:
        pass

    @abstractmethod
    def authenticate(self, jwt_request: JwtRequest) -> JwtResponse | None:
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_request: RefreshJwtRequest) -> JwtResponse | None:
        pass 

    @abstractmethod
    def refresh_refresh_token(self, refresh_request: RefreshJwtRequest) -> JwtResponse | None:
        pass