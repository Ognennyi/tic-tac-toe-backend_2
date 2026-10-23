from domain.model.sign_up_request import SignUpRequest
from domain.service.auth_service import AuthService
from domain.service.user_service import UserService
from uuid import uuid4, UUID


from web.module.jwt_provider import JwtProvider
from domain.model.JwtRequest import JwtRequest
from domain.model.JwtResponse import JwtResponse
from domain.model.RefreshJwtRequest import RefreshJwtRequest


from domain.model.user import User

from werkzeug.security import generate_password_hash, check_password_hash

class AuthServiceImpl(AuthService):

    def __init__(self, user_service: UserService, jwt_provider: JwtProvider):
        self.user_service = user_service
        self.jwt_provider = jwt_provider

    
    def sign_up(self, request: SignUpRequest) -> bool:
        login = request.login
        password = request.password

        existing_user = self.user_service.get_by_login(login)
        if existing_user is not None:
            return False
        
        password_hash = generate_password_hash(password)

        new_user = User(
            id = uuid4(),
            login=request.login,
            password = password_hash
        )

        self.user_service.create_user(new_user)

        return True

        
    def authenticate(self, jwt_request: JwtRequest) -> JwtResponse | None:
        login = jwt_request.login 
        password = jwt_request.password

        user = self.user_service.get_by_login(login)
        if user is None:
            return None
        
        is_valid = check_password_hash(user.password, password)
        if not is_valid:
            return None

        access_token = self.jwt_provider.generate_access_token(user)
        refresh_token = self.jwt_provider.generate_refresh_token(user)

        return JwtResponse(
            type= "Bearer", 
            access_token= access_token,
            refresh_token= refresh_token 
        )


    def refresh_access_token(self, refresh_request: RefreshJwtRequest) -> JwtResponse | None:
        
        refresh_token = refresh_request.refresh_token

        if not self.jwt_provider.validate_refresh_token(refresh_token):
            return None

        user_uuid = self.jwt_provider.get_user_id(refresh_token)
        if user_uuid is None:
            return None
        
        user = self.user_service.get(user_uuid)
        if user is None:
            return None
        
        new_access_token = self.jwt_provider.generate_access_token(user)
        
        return JwtResponse(
            type="Bearer",
            access_token= new_access_token,
            refresh_token= refresh_token
        )

    
    def refresh_refresh_token(self, refresh_request: RefreshJwtRequest) -> JwtResponse | None:

        refresh_token = refresh_request.refresh_token

        if not self.jwt_provider.validate_refresh_token(refresh_token):
            return None

        user_uuid = self.jwt_provider.get_user_id(refresh_token)
        if user_uuid is None:
            return None
        
        user = self.user_service.get(user_uuid)
        if user is None:
            return None
        
        new_access_token = self.jwt_provider.generate_access_token(user)
        new_refresh_token = self.jwt_provider.generate_refresh_token(user)
        
        return JwtResponse(
            type="Bearer",
            access_token= new_access_token,
            refresh_token= new_refresh_token
        )
