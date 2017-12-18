import json
import datetime
from functools import wraps
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.web.server import NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.python.compat import nativeString, unicode
from ..lib.db.token import Token, AnonymouseToken
from ..lib.db.application import Application, AnonymouseApplication


__all__ = [
    'hasUserToken',
    'hasApplicationToken',
    'isStaff',
    'isAdmin',
    'isSuperAdmin',

    'BasicResource',
    'DetailResource',
    'ListResource',
]


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def hasUserToken(f):
    @wraps(f)
    def wrapper(self, cursor, request, *args, **kwargs):
        if isinstance(request.token, Token):
            return f(self, cursor, request, *args, **kwargs)
        else:
            return self.unAuthorized(request, {'message': 'You must be authorized'})

    return wrapper


def hasApplicationToken(f):
    @wraps(f)
    def wrapper(self, cursor, request, *args, **kwargs):
        if isinstance(request.app, Application):
            return f(self, cursor, request, *args, **kwargs)
        else:
            return self.unAuthorized(request, {'message': 'You must not use side channel!'})

    return wrapper


def isStaff(f):
    @wraps(f)
    def wrapper(self, cursor, request, *args, **kwargs):
        if request.token.is_staff or request.token.is_admin or request.token.is_superadmin:
            return f(self, cursor, request, *args, **kwargs)
        else:
            return self.unAuthorized(request, {'message': 'Insufficient permissions, you must be a staff'})

    return wrapper


def isAdmin(f):
    @wraps(f)
    def wrapper(self, cursor, request, *args, **kwargs):
        if request.token.is_admin or request.is_superadmin:
            return f(self, cursor, request, *args, **kwargs)
        else:
            return self.unAuthorized(request, {'message': 'Insufficient permissions, you must be a admin'})

    return wrapper


def isSuperAdmin(f):
    @wraps(f)
    def wrapper(self, cursor, request, *args, **kwargs):
        if request.token.is_superadmin:
            return f(self, cursor, request, *args, **kwargs)
        else:
            return self.unAuthorized(request, {'message': 'Insufficient permissions, you must be a superadmin'})

    return wrapper


class BasicResource(Resource):
    allowedMethods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def jsonResponse(self, request, data):
        request.setHeader("content-type", "application/json; charset=utf-8")
        request.write(
            json.dumps(data, default=json_serial).encode('utf8')
        )
        request.finish()

    def unAuthorized(self, request, message={'error': 'unAuthorized'}):
        request.setResponseCode(403, 'Forbiden'.encode('utf8'))
        self.jsonResponse(request, message)

    def notFound(self, request, message={'error': 'notFound'}):
        request.setResponseCode(404, 'NotFound'.encode('utf8'))
        self.jsonResponse(request, message)

    def notAllowed(self, request, message={'error': 'Method is not allowed'}):
        request.setResponseCode(405, 'NotAllowed'.encode('utf8'))
        self.jsonResponse(request, message)

    def render(self, request):
        m = getattr(self, 'render_' + nativeString(request.method), None)
        if m is None:
            self.notAllowed(request)
        else:
            self.manager.db.runInteraction(self.process, request, m)

        return NOT_DONE_YET

    @inlineCallbacks
    def process(self, cursor, request, method):
        '''
        '''
        application_token = request.getCookie(b'OAUTH_APP')
        application_token = request.getHeader(b'X_OAUTH_APP') or application_token
        if application_token:
            application_token = application_token.decode('utf8')

        user_token = request.getCookie(b'OAUTH_USER')
        user_token = request.getHeader(b'X_OAUTH_USER') or user_token
        if user_token:
            user_token = user_token.decode('utf8')

        request.app = yield Application.getByToken(cursor, application_token)
        request.token = yield Token.getValid(cursor, user_token, request.app.id_application)

        reactor.callLater(2, method, cursor, request)
        #yield method(cursor, request)


class DetailResource(BasicResource):
    isLeaf = True

    def __init__(self, manager, id=None):
        super(DetailResource, self).__init__()
        self.manager = manager
        self.id = id


class ListResource(BasicResource):
    DETAIL = DetailResource

    def getChild(self, name, request):
        if name == b'':
            return self

        else:
            return self.DETAIL(self.manager, name)

