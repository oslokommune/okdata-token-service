Token Service
======================

REST API for creating access tokens in Keycloak from user and client credentials.

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

The service is defined in `template.yaml` and deployed with the [AWS SAM
CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
Per-environment settings (stack name, deployment bucket, region) live in
`samconfig.toml`.

The Lambda functions run a Docker image built from `Dockerfile`. `sam build`
builds the image and `sam deploy` pushes it to the ECR repository
`serverless-token-service-<stage>` (managed in dataplatform-config) before
updating the stack.

Deploy to both dev and prod is automatic via GitHub Actions on push to
`main`. You can alternatively deploy from local machine with: `make deploy` or
`make deploy-prod`. This requires the SAM CLI and Docker.

The GitHub deploy role can only update an existing stack: it is not allowed to
create IAM roles. The first deployment to an environment must therefore be done
from a local machine with administrator access.

The REST API is named `<stage>-token-service`. The `api-gateway-domain` module
in dataplatform-config looks it up by that name to map it to
`api.data[-dev].oslo.systems/token-service`, so after the API has been
(re)created, dataplatform-config must be re-applied to point the domain at the
new API.

## Input event

Input event is a [lambda http proxy request event](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format) with body:
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
