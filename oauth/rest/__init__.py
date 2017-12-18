from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.util import Redirect

from .application import ApplicationListResource
from .token import TokenListResource


class RestResource(Resource):
    def __init__(self, manager):
        self.manager = manager
        Resource.__init__(self)
        self.putChild(b'application', ApplicationListResource(manager))
        self.putChild(b'token', TokenListResource(manager))

    def getChild(self, name, request):
        if name == b'':
            return self

        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        request.setResponseCode(400, b'Bad Request ')
        return b'BAD REQUEST'


