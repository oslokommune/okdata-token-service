import json
from jsonschema import validate, ValidationError


def read_schema(filepath):
    with open(filepath) as f:
        return json.loads(f.read())


def validate_request_body(body, schema):
    try:
        validate(body, schema)
    except ValidationError:
        return lambda_http_proxy_response(
            400, json.dumps({"message": "Invalid request body"})
        )
    return None


def lambda_http_proxy_response(status_code, response_body):
    return {"statusCode": status_code, "body": response_body}


def invalid_json_body_error_response():
    return lambda_http_proxy_response(
        status_code=400, response_body="Invalid JSON in request body"
    )
