import json
from keycloak.exceptions import KeycloakAuthenticationError

create_user_token_event = {
    "body": json.dumps({"username": "username", "password": "password"})
}
refresh_user_token_http_event = {
    "body": json.dumps({"refresh_token": "somerefreshtoken"})
}

create_client_token_event = {
    "body": json.dumps({"client_id": "username", "client_secret": "password"})
}
refresh_client_token_http_event = {
    "body": json.dumps(
        {
            "client_id": "username",
            "client_secret": "password",
            "refresh_token": "somerefreshtoken",
        }
    )
}

keycloak_authorized_response = {
    "access_token": "yo",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "yo",
    "token_type": "bearer",
    "not-before-policy": 1563194597,
    "session_state": "yo",
    "scope": "profile email",
}

ok_response = {"statusCode": 200, "body": json.dumps(keycloak_authorized_response)}

unauthorized_response_body = json.dumps({"message": "Unauthorized"})


def keycloak_auth_error(*args, **kwargs):
    raise KeycloakAuthenticationError("Unauthorized")


unauthorized_response = {"statusCode": 401, "body": unauthorized_response_body}

http_event_invalid_body = {
    "body": json.dumps({"cake": "username", "donut": "password"})
}

bad_request_response = {
    "statusCode": 400,
    "body": json.dumps({"message": "Invalid request body"}),
}
