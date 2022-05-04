from .errors import InvalidNameError


class Player:
    """
    Class Player. Contains attributes:

    :param name: player's nickname
    :type name: str

    :param sign: player's sign used during game
    :type sign: str
    """
    def __init__(self, name: str, sign: str):
        if name:
            self._name = name
        else:
            raise InvalidNameError('Invalid name chosen')
        self._sign = sign

    def name(self):
        return self._name

    def sign(self):
        return self._sign
