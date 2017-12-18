# -*- coding: utf-8 -*-
import random
import string
import datetime
from twisted.python import log
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from .model import Model


class Token(Model):
    NAME = 'public.token'
    ID = 'id_token'

    @staticmethod
    @inlineCallbacks
    def getValid(cursor, token, id_application):
        if token is None:
            returnValue(AnonymouseToken(id_application))
            return

        now = datetime.datetime.now()
        yield cursor.execute(
            '''
            SELECT
                T.id_token, T.id_application, T.id_user, T.validated, T.token, T.created, T.last_activity, T.expiration,
                U.username, U.is_device, AU.is_staff, AU.is_admin, U.is_superadmin
            FROM
                public.token T
                LEFT JOIN public.user U ON U.id_user = T.id_user
                LEFT JOIN public.application A ON T.id_application = A.id_application
                LEFT JOIN public.application_user AU ON T.id_application = AU.id_application AND T.id_user = T.id_user

            WHERE
                T.token = %s
                AND (T.expiration >= now() OR T.expiration IS NULL)
            ORDER BY
                T.created
            LIMIT 1
            ''',
            (token, )
        )

        if cursor.rowcount > 0:
            token = Token(**cursor.fetchone())
            yield token.refresh(cursor)
            return returnValue(token)

        returnValue(AnonymouseToken)

    @staticmethod
    @inlineCallbacks
    def getApplicationUserList(cursor, id_application, id_user):
        yield cursor.execute(
            '''
            SELECT
                T.id_token, T.id_application, T.id_user, T.validated, T.token, T.created, T.last_activity, T.expiration,
                U.username, U.is_device, AU.is_staff, AU.is_admin, U.is_superadmin
            FROM
                public.token T
                LEFT JOIN public.user U ON U.id_user = T.id_user
                LEFT JOIN public.application A ON T.id_application = A.id_application
                LEFT JOIN public.application_user AU ON T.id_application = AU.id_application AND T.id_user = T.id_user

            WHERE
                (T.expiration >= now() OR T.expiration IS NULL)
                AND T.id_application = %s AND T.id_user = %s
            ORDER BY
                T.created
            ''',
            (id_application, id_user)
        )

        if cursor.rowcount > 0:
            return returnValue([Token(**row) for row in cursor.fetchall()])

        return returnValue(AnonymouseToken(id_application))

    @staticmethod
    @inlineCallbacks
    def getUserList(cursor, id_user):
        yield cursor.execute(
            '''
            SELECT
                T.id_token, T.id_application, T.id_user, T.validated, T.token, T.created, T.last_activity, T.expiration,
                U.username, U.is_device, AU.is_staff, AU.is_admin, U.is_superadmin
            FROM
                public.token T
                LEFT JOIN public.user U ON U.id_user = T.id_user
                LEFT JOIN public.application A ON T.id_application = A.id_application
                LEFT JOIN public.application_user AU ON T.id_application = AU.id_application AND T.id_user = T.id_user

            WHERE
                (T.expiration >= now() OR T.expiration IS NULL)
                AND T.id_user = %s
            ORDER BY
                T.created
            ''',
            (id_user, )
        )

        return returnValue([Token(**row) for row in cursor.fetchall()])

    @staticmethod
    @inlineCallbacks
    def create(self, cursor, id_user, id_application):
        pass

    @staticmethod
    @inlineCallbacks
    def remove(self, cursor, id_user, id_application, id_token):
        pass

    def __init__(self, **kwargs):
        self.username = 'Anonymouse'
        self.id_user = 0
        self.id_application = 0
        self.is_device = False
        self.is_staff = False
        self.is_admin = False
        self.is_superadmin = False
        self.last_activity = datetime.datetime.now()
        self.expiration = self.last_activity

        self.__dict__.update(kwargs)

        self.is_staff = self.is_staff or self.is_admin or self.is_superadmin
        self.is_admin = self.is_admin or self.is_superadmin


    @inlineCallbacks
    def refresh(self, cursor):
        yield cursor.execute(
            '''
            UPDATE
                public.token
            SET
                last_activity = now(),
                expiration = now() + A.alive * INTERVAL '1 seconds'
            FROM public.application A
            WHERE
                id_token = %s and A.id_application = public.token.id_application
                RETURNING public.token.last_activity, public.token.expiration
            ''',
            (self.id_token,)
        )

        self.__dict__.update(**cursor.fetchone())


class AnonymouseToken(Token):

    def __init__(self, id_application):
        super(AnonymouseToken, self).__init__(id_application=id_application)

    @inlineCallbacks
    def refresh(self, cursor):
        pass
