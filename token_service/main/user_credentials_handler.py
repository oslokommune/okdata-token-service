import json

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import (
    logging_wrapper,
    log_add,
    log_duration,
    hide_suffix,
)

from token_service.main.keycloak_client import UserTokenClient
from token_service.main.request_utils import (
    invalid_json_body_error_response,
    lambda_http_proxy_response,
    read_schema,
    validate_request_body,
)

create_token_request_schema = read_schema(
    "serverless/documentation/schemas/createUserTokenRequest.json"
)
refresh_token_request_schema = read_schema(
    "serverless/documentation/schemas/refreshUserTokenRequest.json"
)

patch_all()


@logging_wrapper
@xray_recorder.capture("create_token")
def create_token(event, context):
    try:
        body = json.loads(event["body"])
    except json.decoder.JSONDecodeError:
        return invalid_json_body_error_response()

    if error_response := validate_request_body(body, create_token_request_schema):
        return error_response

    log_add(username=hide_suffix(body["username"]))

    token_client = UserTokenClient()
    res, status = log_duration(
        lambda: token_client.request_token(body["username"], body["password"]),
        "keycloak_request_token_duration",
    )

    return lambda_http_proxy_response(status_code=status, response_body=res)


@logging_wrapper
@xray_recorder.capture("refresh_token")
def refresh_token(event, context):
    try:
        body = json.loads(event["body"])
    except json.decoder.JSONDecodeError:
        return invalid_json_body_error_response()

    if error_response := validate_request_body(body, refresh_token_request_schema):
        return error_response

    token_client = UserTokenClient()
    res, status = log_duration(
        lambda: token_client.refresh_token(body["refresh_token"]),
        "keycloak_refresh_token_duration",
    )

    return lambda_http_proxy_response(status_code=status, response_body=res)
