"""
Orion core exceptions
"""

# Internal

class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass


# Commands

class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a, **kw):
        self.print_help = kw.pop('print_help', True)
        super(UsageError, self).__init__(*a, **kw)


# Graph

class VertexDoesNotExists(Exception):
    """To indicate user specified an invalid (non-existing) vertex"""
    pass


class EdgeDoesNotExists(Exception):
    """To indicate user specified an invalid (non-existing) edge"""
    pass


class PropertyDoesNotExists(Exception):
    """To indicate user specified an invalid (non-existing) edge"""
    pass
