from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.util import Redirect

class Auth(Resource):
    isLeaf = True

    def __init__(self, manager):
        self.manager = manager
        Resource.__init__(self)

    def render_GET(self, request):
        return b'Kokot funguje'
