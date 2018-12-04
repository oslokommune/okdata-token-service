from sanic import Sanic
from sanic import response
from sanic.response import json
from sanic_swagger import (
    openapi_blueprint,
    swagger_blueprint
)
import keycloak_client
from models import *

app = Sanic(__name__, strict_slashes=True)

app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

app.config.API_TITLE = "Token Service"
app.config.API_DESCRIPTION = "Provides Access and Refresh tokens. For use with machine resources."



@app.route("/", methods=['GET'])
@doc.route(exclude=True)
async def index(request):
    return response.redirect('/swagger')


@app.route("/tokens/", methods=['POST'])
@doc.consumes(Credentials, location="body")
@doc.tag(name="Tokens")
@doc.response('200', 'Returns Token, Refresh token + metadata', model=TokenResponse)
@doc.response('401', 'Returns Error and error message', model=ErrorResponse)
async def post_event(request):
    body = json.loads(request.body)
    res, status = keycloak_client.get_token(body['username'], body['password'])
    return response.json(res, status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
