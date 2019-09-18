import json
import logging

import token_service.main.keycloak_client as keycloak_client
from jsonschema import validate, ValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


with open("serverless/documentation/schemas/createTokenRequest.json") as f:
    create_token_request_schema = json.loads(f.read())

def handler(event, context):

    try:
        body = json.loads(event["body"])
        validate(body, create_token_request_schema)
    except ValidationError as e:
        logger.exception(f"JSON document does not conform to the given schema: {e}")
        return lambda_http_proxy_response(400, {"message": "Invalid request body"})

    res, status = keycloak_client.get_token(body["username"], body["password"])

    return lambda_http_proxy_response(status_code=status, response_body=res)


def lambda_http_proxy_response(status_code, response_body):
    return {
        "statusCode": status_code,
        "body": json.dumps(response_body)
    }
