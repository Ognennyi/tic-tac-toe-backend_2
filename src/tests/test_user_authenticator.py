from uuid import uuid4
from unittest.mock import Mock


from web.module.jwt_provider import JwtProvider
from web.module.user_authenticator import UserAuthenticator


def test_authenticate_success():
    jwt_provider = Mock(spec=JwtProvider)

    expected_id = uuid4()
    token = "valid_access_token"

    jwt_provider.validate_access_token.return_value = True
    jwt_provider.get_user_id.return_value = expected_id

    authenticator = UserAuthenticator(jwt_provider)

    result = authenticator.authenticate(
        f"Bearer {token}"
    )

    assert result == expected_id

    jwt_provider.validate_access_token.assert_called_once_with(token)
    jwt_provider.get_user_id.assert_called_once_with(token)



def test_authenticate_without_header():
    jwt_provider = Mock(spec=JwtProvider)

    authenticator = UserAuthenticator(jwt_provider)

    result = authenticator.authenticate(None)

    assert result is None

    jwt_provider.validate_access_token.assert_not_called()
    jwt_provider.get_user_id.assert_not_called()


def test_authenticate_wrong_scheme():
    jwt_provider = Mock(spec=JwtProvider)

    authenticator = UserAuthenticator(jwt_provider)

    result = authenticator.authenticate(
        "Basic some_token"
    )

    assert result is None

    jwt_provider.validate_access_token.assert_not_called()
    jwt_provider.get_user_id.assert_not_called()


def test_authenticate_invalid_token():
    jwt_provider = Mock(spec=JwtProvider)

    token = "invalid_token"

    jwt_provider.validate_access_token.return_value = False

    authenticator = UserAuthenticator(jwt_provider)

    result = authenticator.authenticate(
        f"Bearer {token}"
    )

    assert result is None

    jwt_provider.validate_access_token.assert_called_once_with(token)
    jwt_provider.get_user_id.assert_not_called()


def test_authenticate_empty_bearer():
    jwt_provider = Mock(spec=JwtProvider)

    authenticator = UserAuthenticator(jwt_provider)

    result = authenticator.authenticate("Bearer ")

    assert result is None

    jwt_provider.validate_access_token.assert_not_called()
    jwt_provider.get_user_id.assert_not_called()