import json
import os

from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError


class TokenClient:
    server_url = os.environ["KEYCLOAK_SERVER"] + "/auth/"
    realm_name = os.environ["KEYCLOAK_REALM"]

    openid_client: KeycloakOpenID

    def refresh_token(self, refr_token):
        try:
            res = self.openid_client.refresh_token(refresh_token=refr_token)
            return json.dumps(res), 200
        except KeycloakAuthenticationError:
            return json.dumps({"message": "Unauthorized"}), 401


class UserTokenClient(TokenClient):
    def __init__(self):
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        self.openid_client = KeycloakOpenID(
            server_url=self.server_url,
            realm_name=self.realm_name,
            client_id=client_id,
            client_secret_key=client_secret,
        )

    def request_token(self, username, password):
        try:
            res = self.openid_client.token(username=username, password=password)
            return json.dumps(res), 200
        except KeycloakAuthenticationError:
            return json.dumps({"message": "Unauthorized"}), 401


class ClientTokenClient(TokenClient):
    def __init__(self, client_id, client_secret):
        self.openid_client = KeycloakOpenID(
            server_url=self.server_url,
            realm_name=self.realm_name,
            client_id=client_id,
            client_secret_key=client_secret,
        )

    def request_token(self):
        try:
            res = self.openid_client.token(grant_type=["client_credentials"])
            return json.dumps(res), 200
        except KeycloakAuthenticationError:
            return json.dumps({"message": "Unauthorized"}), 401
