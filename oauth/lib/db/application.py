# -*- coding: utf-8 -*-
import random
import string
import datetime
from twisted.python import log
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from .model import Model


class Application(Model):
    NAME = 'public.application'
    ID = 'id_application'

    @staticmethod
    @inlineCallbacks
    def getByToken(cursor, token):
        if token is None:
            returnValue(AnonymouseApplication())
            return

        now = datetime.datetime.now()
        yield cursor.execute(
            '''
            SELECT
            *
                A.*
            FROM
                public.application A
            WHERE
                A.token = %s
            ORDER BY
                T.created
            LIMIT 1
            ''',
            (token, )
        )

        if cursor.rowcount > 0:
            token = Application(**cursor.fetchone())
            yield token.refresh(cursor)
            returnValue(token)
        else:
            returnValue(AnonymouseApplication())


class AnonymouseApplication(Application):

    def __init__(self):
        self.id_application = None
