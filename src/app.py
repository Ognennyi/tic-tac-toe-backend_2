from flask import Flask, request

from web.route.game_route import create_game_blueprint
from di.container import Container

from web.route.auth_controller import create_auth_blueprint

from web.route.user_route import create_user_blueprint

from web.module.user_authenticator import UserAuthenticator

from flask import g


from flask_jwt_extended import JWTManager
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)




app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

container = Container()
game_blueprint = create_game_blueprint(container.service, container.user_service)
app.register_blueprint(game_blueprint)

auth_blueprint = create_auth_blueprint(container.auth_service)
app.register_blueprint(auth_blueprint)

user_blueprint = create_user_blueprint(container.user_service)
app.register_blueprint(user_blueprint)


authenticator = UserAuthenticator(container.jwt_provider) 


@app.before_request
def check_authentication():

    if request.endpoint == "auth.auth_sign_up" or request.endpoint == "auth.auth_login" or request.endpoint == "auth.refresh_access_token" or request.endpoint == "auth.refresh_refresh_token":
        return None
    
    authorization_string = request.headers.get("Authorization")

    if authorization_string is None:
        return{
            "message": "Authorization error"
        }, 401, {
                    "WWW-Authenticate": 'Bearer realm="TicTacToe"'
                }
    
    user_id = authenticator.authenticate(authorization_string)

    if user_id is not None:
        g.user_id = user_id
        return None
    else:
        return{
            "message": "Authorization error"
        }, 401, {
                    "WWW-Authenticate": 'Bearer realm="TicTacToe"'
                }




if __name__ == "__main__":
    app.run(debug=True)

