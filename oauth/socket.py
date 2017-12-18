from twisted.internet import reactor

class Connection(object):

    def connect(self, site):
        pass


class ConnectionTCP(Connection):

    def __init__(self, ip='0.0.0.0', port=5050):
        self.ip = ip
        self.port = port

    def connect(self, site):
        reactor.listenTCP(self.port, site)


class ConnectionUnixSocket(Connection):

    def __init__(self, path):
        self.path = path

    def connect(self, site):
        reactor.listenUNIX(self.path, site)
