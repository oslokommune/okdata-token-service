import json
import logging

import token_service.main.keycloak_client as keycloak_client
from jsonschema import validate, ValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


with open("serverless/documentation/schemas/createTokenRequest.json") as f:
    create_token_request_schema = json.loads(f.read())


with open("serverless/documentation/schemas/refreshTokenRequest.json") as f:
    refresh_token_request_schema = json.loads(f.read())


def handle(event, context):
    body = json.loads(event["body"])

    validate_error_response = validate_request_body(body, create_token_request_schema)

    if validate_error_response:
        return validate_error_response

    res, status = keycloak_client.get_token(body["username"], body["password"])

    return lambda_http_proxy_response(status_code=status, response_body=res)


def handle_refresh_token(event, context):

    body = json.loads(event["body"])

    validate_error_response = validate_request_body(body, refresh_token_request_schema)

    if validate_error_response:
        return validate_error_response

    res, status = keycloak_client.refresh_token(body["refresh_token"])

    return lambda_http_proxy_response(status_code=status, response_body=res)


def validate_request_body(body, schema):
    try:
        validate(body, schema)
    except ValidationError as e:
        logger.exception(f"JSON document does not conform to the given schema: {e}")
        return lambda_http_proxy_response(
            400, json.dumps({"message": "Invalid request body"})
        )


def lambda_http_proxy_response(status_code, response_body):
    return {"statusCode": status_code, "body": response_body}
