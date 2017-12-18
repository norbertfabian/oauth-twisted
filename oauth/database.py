import psycopg2
import psycopg2.extras

from twisted.python import log
from txpostgres import txpostgres, reconnection
from .lib.db.token import Token
import json


class DictConnection(txpostgres.Connection):

    @staticmethod
    def connectionFactory(*args, **kwargs):
        kwargs['cursor_factory'] = psycopg2.extras.DictCursor
        return psycopg2.connect(*args, **kwargs)


class LoggingDetector(reconnection.DeadConnectionDetector):

    def startReconnecting(self, f):
        log.msg('[*] database connection is down (error: %r)' % f.value)
        return reconnection.DeadConnectionDetector.startReconnecting(self, f)

    def reconnect(self):
        log.msg('[*] reconnecting...')
        return reconnection.DeadConnectionDetector.reconnect(self)

    def connectionRecovered(self):
        log.msg('[*] connection recovered')
        return reconnection.DeadConnectionDetector.connectionRecovered(self)


def success(res):
    log.msg(res)

def error(f):
    log.err(f.value)


def afterDbConnect(self, db):
    log.msg('Database connected')

def database(connection_string):
    db = DictConnection(detector=LoggingDetector())
    d = db.connect(connection_string)
    d.addErrback(db.detector.checkForDeadConnection)
    d.addCallback(afterDbConnect, db)
    return db


