from flask import Blueprint
from flask.views import MethodView

from app.common.check_auth import check_api_auth
from app.common.api_helpers import json_response


api_resource1 = Blueprint(
    'api_resource1',
    __name__
)


class Resource1Resource(MethodView):

    decorators = [check_api_auth]

    def get(self):
        return json_response({})

api_resource1.add_url_rule(
    '/resources',
    view_func=Resource1Resource.as_view('resource1')
)
