import os
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.web.util import Redirect
from autobahn.twisted.resource import WebSocketResource

from .html import HtmlResource
from .rest import RestResource


class ApiResource(Resource):

    def __init__(self, manager):
        super(ApiResource, self).__init__()

        self.manager = manager
        self.putChild(b'html', HtmlResource(manager))
        self.putChild(b'rest', RestResource(manager))


class RootResource(Resource):

    def __init__(self, manager):
        super(RootResource, self).__init__()

        self.manager = manager
        self.putChild(b'static', File(os.path.dirname(os.path.realpath(__file__)) + '/static/'))
        self.putChild(b'api', ApiResource(manager))

    def getChild(self, name, request):
        return Redirect(b'api/html/')
