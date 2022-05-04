class Score:
    """
    Class Score. Contains attributes:

    :param player_name: player's name
    :type player_name: str

    :param moves: count of player's moves
    :type moves: int
    """
    def __init__(self, player_name, moves):
        self._player_name = player_name
        self._moves = moves

    def player_name(self):
        return self._player_name

    def moves(self):
        return self._moves

    def __str__(self):
        player = self.player_name()
        moves = self.moves()
        return f'Winner: {player}, Moves count: {moves}'
