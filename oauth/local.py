try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def getManager():
    return getattr(_thread_locals, 'manager', None)


def setManager(manager):
    _thread_locals.manager = manager

