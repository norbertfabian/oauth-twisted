from twisted.python import log
from twisted.internet.defer import Deferred, inlineCallbacks
from .model import Model


class Contact(Model):
    NAME = 'public.contact'
    ID = 'id_contact'

    @staticmethod
    def getUserContact(cursor, id_user, id_contact):
        query = cursor.execute(
            '''
            ''',
            (id, )
        )

    @staticmethod
    def getApplicationContact(cursor, id_application, id_contact):
        pass

    @staticmethod
    def getApplicationContactList(cursor, id_application, hide_old=True):
        pass

    def getApplicationUserContactList(cursor, id_application, id_user, hide_old=True):
        pass

    def getHash(self):
        pass

    def save(self, cursor):
        pass
