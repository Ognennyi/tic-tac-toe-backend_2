from domain.model.user import User
from uuid import UUID

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

class JwtProvider:


    def generate_access_token(self, user: User)-> str:
        
        user_id = str(user.id)
        access_token = create_access_token(identity=user_id)
        return access_token
    

    def generate_refresh_token(self, user: User)-> str:
        user_id = str(user.id)
        refresh_token = create_refresh_token(identity=user_id)
        return refresh_token

    def validate_access_token(self, token: str) -> bool:
        try:
            decode = decode_token(token) #словарь
            return decode["type"] == "access"
        except Exception:
            return False

    def validate_refresh_token(self, token: str) -> bool:
        try:
            decode = decode_token(token) #словарь
            return decode["type"] == "refresh"
        except Exception:
            return False

    def get_user_id(self, token: str) -> UUID | None:
        try:
            decode = decode_token(token)
            return UUID(decode["sub"])
        except Exception:
            return None