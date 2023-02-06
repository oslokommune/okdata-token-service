from keycloak import KeycloakOpenID

import token_service.main.user_credentials_handler as handler

from token_service.test.test_data import (
    keycloak_authorized_response,
    create_user_token_event,
    ok_response,
    keycloak_auth_error,
    unauthorized_response,
    http_event_invalid_body,
    bad_request_response,
    refresh_user_token_http_event,
)

from aws_xray_sdk.core import xray_recorder

xray_recorder.begin_segment("Test")


class TestUserCredentialsHandler:
    def test_create_token_ok(self, mocker):
        mocker.patch.object(KeycloakOpenID, "token")
        KeycloakOpenID.token.return_value = keycloak_authorized_response

        response = handler.create_token(create_user_token_event, {})

        assert response == ok_response

    def test_create_token_unauthorized(self, mocker):
        mocker.patch.object(KeycloakOpenID, "token", new=keycloak_auth_error)

        response = handler.create_token(create_user_token_event, {})

        assert response == unauthorized_response

    def test_create_token_invalid_body(self):
        response = handler.create_token(http_event_invalid_body, {})

        assert response == bad_request_response

    def test_refresh_token_ok(self, mocker):
        mocker.patch.object(KeycloakOpenID, "refresh_token")
        KeycloakOpenID.refresh_token.return_value = keycloak_authorized_response

        response = handler.refresh_token(refresh_user_token_http_event, {})

        assert response == ok_response

    def test_refresh_token_unauthorized(self, mocker):
        mocker.patch.object(KeycloakOpenID, "refresh_token")
        KeycloakOpenID.refresh_token.side_effect = keycloak_auth_error

        response = handler.refresh_token(refresh_user_token_http_event, {})

        assert response == unauthorized_response

    def test_refresh_token_invalid_body(self):
        response = handler.refresh_token(http_event_invalid_body, {})

        assert response == bad_request_response
