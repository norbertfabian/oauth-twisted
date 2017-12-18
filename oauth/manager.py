# -*- coding: utf-8 -*-

import os
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue, Deferred
from twisted.web.server import Site
from .resource import RootResource
from .database import database
from .socket import ConnectionTCP, ConnectionUnixSocket


class Manager(object):

    def __init__(self, config, socket=ConnectionTCP()):
        self.socket = socket
        self.db = database(config['DB'])

        root = RootResource(self)
        self.site = Site(root)

    def sleep(self, time):
        d = Deferred()
        reactor.callLater(time, d.callback, None)
        return d

    def run(self):
        self.socket.connect(self.site)
        return reactor.run()
