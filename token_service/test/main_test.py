from keycloak import KeycloakOpenID

import token_service.main.handler as handler

from token_service.test.main_test_data import (
    keycloak_authorized_response,
    http_event,
    ok_response,
    keycloak_auth_error,
    unauthorized_response,
    http_event_invalid_body,
    bad_request_response,
)


class TestHandler:
    def test_ok(self, mocker):
        mocker.patch.object(KeycloakOpenID, "token")
        KeycloakOpenID.token.return_value = keycloak_authorized_response

        response = handler.handle(http_event, {})

        assert response == ok_response

    def test_unauthorized(self, mocker):
        mocker.patch.object(KeycloakOpenID, "token", new=keycloak_auth_error)

        response = handler.handle(http_event, {})

        assert response == unauthorized_response

    def test_invalid_body(self):

        response = handler.handle(http_event_invalid_body, {})

        assert response == bad_request_response
