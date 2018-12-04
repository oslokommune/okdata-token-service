from sanic import Sanic
from sanic import response
from sanic.response import json
import json
import keycloak_client

app = Sanic(__name__)


@app.route("/tokens/", methods=['POST'])
async def post_event(request):
    body = json.loads(request.body)
    res, status = keycloak_client.get_token(body['username'], body['password'])
    return response.json(res, status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
