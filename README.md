Token Service
======================

REST API for creating access tokens in Keycloak from user and client credentials.

## Setup

1. [Install Serverless Framework](https://serverless.com/framework/docs/getting-started/)
2. Install plugins:
```
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-aws-documentation
```

## Running tests

Tests are run using [tox](https://pypi.org/project/tox/).

```
$ tox
```
Or
```
$ make test
```

## Deploy

Deploy to both dev and prod is automatic via GitHub Actions on push to
`main`. You can alternatively deploy from local machine with: `make deploy` or
`make deploy-prod`.

## Input event

Input event is a [lambda http proxy request event](https://serverless.com/framework/docs/providers/aws/events/apigateway/#example-lambda-proxy-event-default) with body:
```json
{
  "username": "user1",
  "password": "password123"
}
```

## Output

Output is a [lambda http proxy response event](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format) with body:
```json
{
    "access_token": "some-access-token",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "some-refresh-token",
    "token_type": "bearer",
    "not-before-policy": 1563194597,
    "session_state": "some-uuid",
    "scope": "profile email"
}
```
