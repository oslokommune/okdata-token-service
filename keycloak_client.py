import json
import os

from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from sanic.log import logger


server_url = os.environ['KEYCLOAK_SERVER']
client_id = os.environ['CLIENT_ID']
realm_name = os.environ['KEYCLOAK_REALM']
client_secret = os.environ['CLIENT_SECRET']

# Configure client
token_service_client = KeycloakOpenID(server_url=server_url,
                                      client_id=client_id,
                                      realm_name=realm_name,
                                      client_secret_key=client_secret)


def get_token(username, password):
    logger.info(token_service_client.client_id)
    try:
        return token_service_client.token(username, password), 200
    except KeycloakAuthenticationError as ke:
        logger.info(ke)
        return json.loads(ke.response_body), ke.response_code
