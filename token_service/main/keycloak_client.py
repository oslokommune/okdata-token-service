import json
import os


from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError


server_url = os.environ["KEYCLOAK_SERVER"]
client_id = os.environ["CLIENT_ID"]
realm_name = os.environ["KEYCLOAK_REALM"]
client_secret = os.environ["CLIENT_SECRET"]


openid_client = KeycloakOpenID(
    server_url=server_url,
    realm_name=realm_name,
    client_id=client_id,
    client_secret_key=client_secret,
)


def request_token(username, password):
    try:
        res = openid_client.token(username=username, password=password)
        return json.dumps(res), 200
    except KeycloakAuthenticationError:
        return json.dumps({"message": "Unauthorized"}), 401


def refresh_token(refr_token):
    try:
        res = openid_client.refresh_token(refresh_token=refr_token)
        return json.dumps(res), 200
    except KeycloakAuthenticationError:
        return json.dumps({"message": "Unauthorized"}), 401
