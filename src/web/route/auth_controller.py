from flask import Blueprint, request

from domain.model.sign_up_request import SignUpRequest

from domain.service.auth_service import AuthService
from domain.model.JwtRequest import JwtRequest
from domain.model.RefreshJwtRequest import RefreshJwtRequest


def create_auth_blueprint(service: AuthService) -> Blueprint:
    auth_blueprint = Blueprint('auth', __name__)

    @auth_blueprint.post("/auth/signup")
    def auth_sign_up():


        data = request.get_json(silent=True)

        if data is None or not isinstance(data, dict):
            return{
                "message": "Некорректное тело запроса"
            }, 400
        
        if "login" not in data or "password" not in data:
            return{
                "message": "Некорректный запрос (отсутствует логин или пароль)"
            }, 400
        
        
        if not isinstance(data["login"], str) or not isinstance(data["password"], str):
            return{
                "message": "Некорректное тело запроса"
            }, 400
             

        user = SignUpRequest(
            login=data["login"],
            password=data["password"]
        )

        result = service.sign_up(user)

        if result:
            return{
                "message": "Пользователь зарегистрирован"
            }, 201
        else:
            return{
                "message": "Логин уже занят"
            },409
        






    @auth_blueprint.post("/auth/login")
    def auth_login():

        data = request.get_json(silent=True)

        if data is None or "login" not in data or "password" not in data or not isinstance(data, dict) or not isinstance(data["password"],str) or not isinstance(data["login"],str):
            return{
                "message": "Неверные учётные данные"
            }, 400
        
        jwt_request = JwtRequest(data["login"], data["password"])

        jwt_response = service.authenticate(jwt_request)
        if jwt_response is None:
            return{
                "message": "Неверные учётные данные"
            }, 401
        
        return{
                "type": jwt_response.type,
                "accessToken": jwt_response.access_token,
                "refreshToken": jwt_response.refresh_token
            }, 200
    


    @auth_blueprint.post("/auth/refresh/access")
    def refresh_access_token():
        
        data = request.get_json(silent=True)
        if data is None:
            return{
                "message": "Неверные данные1"
            }, 400
        
        if not isinstance(data, dict):
            return{
                "message": "Неверные данные2"
            }, 400
        
        if "refreshToken" not in data or not isinstance(data["refreshToken"], str):
            return{
                "message": "Неверные данные3"
            }, 400
        
        refresh_jwt_request = RefreshJwtRequest(data["refreshToken"])
        jwt_response = service.refresh_access_token(refresh_jwt_request)

        if jwt_response is None:
            return{
                "message": "Неверные данные об refresh_token"
            }, 401
        
        return{
                "type": jwt_response.type,
                "accessToken": jwt_response.access_token,
                "refreshToken": jwt_response.refresh_token
            }, 200
    

    @auth_blueprint.post("/auth/refresh/refresh")
    def refresh_refresh_token():
        
        data = request.get_json(silent=True)
        if data is None:
            return{
                "message": "Неверные данные"
            }, 400
        
        if not isinstance(data, dict):
            return{
                "message": "Неверные данные"
            }, 400
        
        if "refreshToken" not in data or not isinstance(data["refreshToken"], str):
            return{
                "message": "Неверные данные"
            }, 400
        
        
        refresh_jwt_request = RefreshJwtRequest(data["refreshToken"])
        jwt_response = service.refresh_refresh_token(refresh_jwt_request)

        if jwt_response is None:
            return{
                "message": "Неверные данные об refresh_token"
            }, 401
        
        return{
                "type": jwt_response.type,
                "accessToken": jwt_response.access_token,
                "refreshToken": jwt_response.refresh_token
            }, 200


    



    return auth_blueprint



