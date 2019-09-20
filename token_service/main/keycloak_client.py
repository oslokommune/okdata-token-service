import json
import os
import logging

from keycloak.realm import KeycloakRealm
from keycloak.exceptions import KeycloakClientError

server_url = os.environ["KEYCLOAK_SERVER"]
client_id = os.environ["CLIENT_ID"]
realm_name = os.environ["KEYCLOAK_REALM"]
client_secret = os.environ["CLIENT_SECRET"]


logger = logging.getLogger()
logger.setLevel(logging.INFO)

realm = KeycloakRealm(server_url=server_url, realm_name=realm_name)

openid_client = realm.open_id_connect(client_id=client_id, client_secret=client_secret)


def get_token(username, password):
    try:
        res = openid_client.password_credentials(username=username, password=password)
        return json.dumps(res), 200
    except KeycloakClientError as ke:
        logger.exception(f"{ke}")
        return json.dumps({"message": "Unauthorized"}), 401
