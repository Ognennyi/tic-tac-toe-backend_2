from flask import Blueprint
from uuid import UUID
from flask import g
from domain.service.user_service import UserService



def create_user_blueprint(service: UserService) -> Blueprint:
    user_blueprint = Blueprint('users', __name__)

    @user_blueprint.get("/users/<user_id>")
    def get_user_by_id(user_id):
        
        user_id = UUID(user_id)
        user = service.get(user_id)
        if user is None:
            return{
                "message": "Пользователь не найден"
            }, 404
        
        return{
                "id": str(user.id),
                "login": user.login
            }

    @user_blueprint.get("/user/me")
    def get_user_by_access():

        user_id = g.user_id

        user = service.get(user_id)
        if user is None:
            return{
                "message": "errortoken"
            },404
        
        return{
                "id": str(user.id),
                "login": user.login
            },200

    return user_blueprint