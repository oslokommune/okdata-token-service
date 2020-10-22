import json

from aws_xray_sdk.core import patch_all, xray_recorder
from jsonschema import validate, ValidationError
from dataplatform.awslambda.logging import (
    logging_wrapper,
    log_add,
    log_duration,
    hide_suffix,
)

from token_service.main.keycloak_client import ClientTokenClient

with open("serverless/documentation/schemas/createClientTokenRequest.json") as f:
    create_token_request_schema = json.loads(f.read())

with open("serverless/documentation/schemas/refreshClientTokenRequest.json") as f:
    refresh_token_request_schema = json.loads(f.read())

patch_all()


@logging_wrapper("token-service")
@xray_recorder.capture("create_token")
def create_token(event, context):
    body = json.loads(event["body"])

    validate_error_response = validate_request_body(body, create_token_request_schema)

    if validate_error_response:
        return validate_error_response

    log_add(client_id=hide_suffix(body["client_id"]))

    res, status = log_duration(
        lambda: ClientTokenClient(
            client_id=body["client_id"], client_secret=body["client_secret"]
        ).request_token(),
        "keycloak_request_token_duration",
    )

    return lambda_http_proxy_response(status_code=status, response_body=res)


@logging_wrapper("token-service")
@xray_recorder.capture("create_token")
def refresh_token(event, context):
    body = json.loads(event["body"])

    validate_error_response = validate_request_body(body, refresh_token_request_schema)

    if validate_error_response:
        return validate_error_response

    log_add(client_id=hide_suffix(body["client_id"]))

    res, status = log_duration(
        lambda: ClientTokenClient(
            client_id=body["client_id"], client_secret=body["client_secret"]
        ).refresh_token(body["refresh_token"]),
        "keycloak_refresh_token_duration",
    )

    return lambda_http_proxy_response(status_code=status, response_body=res)


def validate_request_body(body, schema):
    try:
        validate(body, schema)
    except ValidationError:
        return lambda_http_proxy_response(
            400, json.dumps({"message": "Invalid request body"})
        )


def lambda_http_proxy_response(status_code, response_body):
    return {"statusCode": status_code, "body": response_body}
