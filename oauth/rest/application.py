from twisted.python import log
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.resource import Resource, ErrorPage
from twisted.web.util import Redirect
from .resource import *
from ..lib.db.token import Token


class ApplicationDetailResource(DetailResource):
    @hasUserToken
    @hasApplicationToken
    @inlineCallbacks
    def render_GET(self, cursor, request):
        if self.id == b'current':
            self.jsonResponse(request, request.token.__dict__)

        elif self.id == b'application':
            token_list = yield Token.getApplicationUserList(
                cursor,
                request.token.id_application,
                request.token.id_user
            )
            self.jsonResponse(request, [token.__dict__ for token in token_list])

        else:
            self.notFound(request)


class ApplicationListResource(ListResource):
    '''
    '''
    DETAIL = ApplicationDetailResource

    def __init__(self, manager):
        super(ApplicationListResource, self).__init__()
        self.manager = manager

    @hasUserToken
    @inlineCallbacks
    def render_GET(self, cursor, request):
        token_list = yield Token.getUserList(cursor, request.token.id_user)
        self.jsonResponse(request, [token.__dict__ for token in token_list])
