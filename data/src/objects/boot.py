from .object import Object


class Boot(Object):
    name = 'brown_boot'

    def __init__(self, game, position):
        Object.__init__(self, game, self.name, position)
