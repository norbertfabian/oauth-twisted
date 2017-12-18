# -*- coding: utf-8 -*-
import random
import string
import datetime
from twisted.python import log
from twisted.internet.defer import Deferred, inlineCallbacks


def getRandom(N=64, choice=string.printable):
    return ''.join(random.choice(choice) for _ in range(N))


class Model(object):
    NAME = 'Table'
    ID = 'id'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def fields(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    def __str__(self):
        return '<%s> %s' % (self.NAME, self.__dict__)

    def __repr__(self):
        return '<%s> %s' % (self.NAME, self.__dict__)
