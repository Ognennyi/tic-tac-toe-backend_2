from uuid import UUID



from web.module.jwt_provider import JwtProvider


class UserAuthenticator():

    def __init__(self, jwt_provider: JwtProvider):
        self.jwt_provider = jwt_provider


    def authenticate(self, authorization: str | None) -> UUID | None:

        if authorization is None:
            return None
        
        parts = authorization.split(" ", 1)

        if len(parts) != 2:
            return None


        if parts[0].lower() == "bearer" and len(parts[1]) != 0:
            if self.jwt_provider.validate_access_token(parts[1]):
                user_uuid = self.jwt_provider.get_user_id(parts[1])
                return user_uuid
            else:
                return None
        else:
            return None