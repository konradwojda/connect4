from .player import Player
from random import randint


class Bot(Player):
    """
    Class Bot. Contains attributes:

    :param sign: bot's sign
    :type sign: str

    """
    def __init__(self, sign: str):
        name = 'Bot'
        super().__init__(name, sign)

    def choose_column(self, width):
        """
        Returns random column number
        """
        return randint(1, width)
