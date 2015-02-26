"""
Refer to http://stackoverflow.com/a/6798042
"""

__author__ = 'grainier'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonGraph(type):
    """
    Graphs behave differently. it shouldn't have a singleton
    for SessionGraph or a BaseGraph. Instead of that it should
    have a singleton per each session (singleton per session or IP)
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        try:
            session = args[0]
            pass
        except IndexError:
            session = "base"
            pass

        if "{0}_{1}".format(cls, session) not in cls._instances:
            print "not in instances"
            cls._instances[
                "{0}_{1}".format(cls, session)
            ] = super(SingletonGraph, cls).__call__(*args, **kwargs)
            pass
        else:
            print "in instances"
            gcls = cls._instances["{0}_{1}".format(cls, session)]
            if not gcls.is_same_session(session):
                print "new instances"
                cls._instances[
                    "{0}_{1}".format(cls, session)
                ] = super(SingletonGraph, cls).__call__(*args, **kwargs)
                pass
            pass
        return cls._instances["{0}_{1}".format(cls, session)]
