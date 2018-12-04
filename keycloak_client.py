import json

from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from sanic.log import logger

# Configure client
token_service_client = KeycloakOpenID(server_url="http://localhost:32768/auth/",
                                      client_id="token-service",
                                      realm_name="dataplattform",
                                      client_secret_key="***REMOVED***")


def get_token(username, password):
    try:
        return token_service_client.token(username, password), 200
    except KeycloakAuthenticationError as ke:
        logger.info(ke)
        return json.loads(ke.response_body), ke.response_code
