
from uuid import uuid4
from app import app



def test_refresh_access():

    client = app.test_client()

    login = f"user_{uuid4()}"
    password = "1234567"

    client.post("/auth/signup",       
        json={
            "login": login,
            "password": password
        }
    )

    login_response = client.post("/auth/login",       
        json={
            "login": login,
            "password": password
        }
    )
    
    login_data = login_response.get_json()

    assert login_response.status_code == 200

    access = login_data["accessToken"]
    refresh = login_data["refreshToken"]

    refresh_access_response = client.post("/auth/refresh/access",       
        json={
            "refreshToken": refresh
        }
    )

    assert refresh_access_response.status_code == 200

    refresh_data = refresh_access_response.get_json()

    assert refresh_data["accessToken"] != access

    assert refresh_data["refreshToken"] == refresh

    assert refresh_data["type"] == "Bearer"
    assert isinstance(refresh_data["accessToken"], str)






def test_refresh_refresh():

    client = app.test_client()

    login = f"user_{uuid4()}"
    password = "1234567"

    client.post("/auth/signup",       
        json={
            "login": login,
            "password": password
        }
    )

    login_response = client.post("/auth/login",       
        json={
            "login": login,
            "password": password
        }
    )
    
    login_data = login_response.get_json()

    assert login_response.status_code == 200

    access = login_data["accessToken"]
    refresh = login_data["refreshToken"]

    headers = {
        "Authorization": f"Bearer {access}"
    }

    refresh_access_response = client.post("/auth/refresh/refresh",       
        json={
            "refreshToken": refresh
        },
        headers=headers
    )

    assert refresh_access_response.status_code == 200

    refresh_data = refresh_access_response.get_json()

    assert refresh_data["accessToken"] != access

    assert refresh_data["refreshToken"] != refresh

    assert refresh_data["type"] == "Bearer"
    assert isinstance(refresh_data["accessToken"], str)
    assert isinstance(refresh_data["refreshToken"], str)