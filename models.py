from sanic_swagger import doc
import json


class Credentials(doc.Model):
    username: str = doc.field(description="PRK username")
    password: str = doc.field(description="PRK password")


class TokenResponse(doc.Model):
    access_token: str = doc.field()
    expires_in: int = doc.field()
    refresh_expires_in: int = doc.field()
    refresh_token: str = doc.field()
    token_type: str = doc.field()
    not_before_policy: int = doc.field(description="Real key is actually 'not-before-policy'")
    session_state: str = doc.field()
    scope: str = doc.field()


class ErrorResponse(doc.Model):
    error: str = doc.field()
    error_description: str = doc.field()