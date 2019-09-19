import json
from keycloak.exceptions import KeycloakAuthenticationError


http_event = {"body": '{"username":"username","password":"password"}'}

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

unauthorized_response_body = {
    "error": "invalid_grant",
    "error_description": "Invalid user credentials",
}

keycloak_auth_error = KeycloakAuthenticationError(
    error_message="Some error message",
    response_body=json.dumps(unauthorized_response_body),
    response_code=401,
)

unauthorized_response = {
    "statusCode": 401,
    "body": json.dumps(unauthorized_response_body),
}

http_event_invalid_body = {"body": '{"cake":"username","donut":"password"}'}

bad_request_response = {
    "statusCode": 400,
    "body": json.dumps({"message": "Invalid request body"}),
}
