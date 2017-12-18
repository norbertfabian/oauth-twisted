from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.util import Redirect
from .auth import Auth

class HtmlResource(Resource):
    def __init__(self, manager):
        self.manager = manager
        Resource.__init__(self)

        self.putChild(b'auth', Auth(manager))
        #self.putChild(b'online', Online(manager))

    def getChild(self, name, request):
        if name == b'':
            return Redirect(b'/api/html/auth/')
        
        return Resource.getChild(self, name, request)

