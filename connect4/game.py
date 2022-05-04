from .board import Board
from .config import WIN_COUNT, WIDTH, HEIGHT
from .errors import InvalidPlayerCount
import random
import numpy as np


class Game:
    """
    Class game. Contains attributes:
    :param players: list of players (2 players only)
    :type players: list

    :param board: board of game
    :type board: Board

    :param height: board's height
    :type height: int

    :param width: board's width
    :type width: int

    :param current_player: player which turn is next
    :type current_player: Player

    :param id: id of the game (only when game is being saved)
    :type id: int
    """
    def __init__(self, players: list, array=None):
        if len(players) == 2:
            self._players = players
        else:
            raise InvalidPlayerCount('Too many players')
        if array is not None:
            self._board = Board(array)
            self._height = self._board.height()
            self._width = self._board.width()
        else:
            self._width = WIDTH
            self._height = HEIGHT
            self._board = Board()
        self._current_player = None
        self._id = None

    def id(self):
        return self._id

    def height(self):
        return self._height

    def width(self):
        return self._width

    def players(self):
        return self._players

    def board(self):
        return self._board

    def current_player(self):
        return self._current_player

    def choose_first_player(self):
        """
        Randomly choices the first player
        """
        self._current_player = random.choice(self.players())

    def get_player_by_sign(self, sign):
        """
        Returns player object by its sign
        Returns Flase if invalid sign has been chosen
        """
        for player in self.players():
            if player.sign() == sign:
                return player
        return False

    def get_player_by_name(self, name):
        """
        Returns player object by its name
        Returns Flase if invalid name has been chosen
        """
        for player in self.players():
            if player.name() == name:
                return player
        return False

    def toggle(self):
        """
        Toggles current player to other one
        """
        current_player = self.current_player()
        players_list = self.players()
        if players_list.index(current_player) == 0:
            self._current_player = self.players()[1]
        else:
            self._current_player = self.players()[0]

    def check_function(self, x_range_start, x_range_stop,
                       y_range_start, y_range_stop, type):
        """
        General figure to check if there are WIN_COUNT signs next to each other
        """
        first_sign = self.players()[0].sign()
        second_sign = self.players()[1].sign()
        board = self.board().board()
        for x in range(x_range_start, x_range_stop):
            for y in range(y_range_start, y_range_stop):
                signs_list = []
                index = 0
                for _ in range(WIN_COUNT):
                    if type == 'horizontal':
                        signs_list.append(board[x][y+index])
                    if type == 'diag_right':
                        signs_list.append(board[x-index][y+index])
                    if type == 'diag_left':
                        signs_list.append(board[x+index][y+index])
                    index += 1
                if len(set(signs_list)) == 1:
                    if signs_list[0] == first_sign:
                        return first_sign
                    if signs_list[0] == second_sign:
                        return second_sign
        return False

    def check_horizontal(self):
        """
        Checks if there are WIN_COUNT signs next to each other horizontally
        Returns sign if there are
        Else returns False
        """
        x_range_start = 0
        x_range_stop = self.height()
        y_range_stop = self.width()-WIN_COUNT+1
        y_range_start = 0
        type = 'horizontal'
        winner = self.check_function(x_range_start, x_range_stop,
                                     y_range_start, y_range_stop, type)
        return winner

    def check_vertical(self):
        """
        Checks if there are WIN_COUNT signs next to each other vertically
        Returns sign if there are
        Else returns False
        """
        height = self._height
        width = self._width
        self._board._board = self.board().board().transpose()
        self._width = height
        self._height = width
        winning = self.check_horizontal()
        self._board._board = self.board().board().transpose()
        self._width = width
        self._height = height
        return winning

    def check_diagonal_right(self):
        """
        Checks if there are WIN_COUNT sign next to
        each other diagonally up-right (/)
        Returns sign if there are
        Else returns False
        """
        x_range_start = WIN_COUNT-1
        x_range_stop = self.height()
        y_range_start = 0
        y_range_stop = self.width()-WIN_COUNT+1
        type = 'diag_right'
        winner = self.check_function(x_range_start, x_range_stop,
                                     y_range_start, y_range_stop, type)
        return winner

    def check_diagonal_left(self):
        """
        Checks if there are WIN_COUNT sign next to
        each other diagonally up-left (\\)
        Returns sign if there are
        Else returns False
        """
        x_range_start = 0
        x_range_stop = self.height()-WIN_COUNT+1
        y_range_start = 0
        y_range_stop = self.width()-WIN_COUNT+1
        type = 'diag_left'
        winner = self.check_function(x_range_start, x_range_stop,
                                     y_range_start, y_range_stop, type)
        return winner

    def check_winner(self):
        """
        Checks if there is a winner
        Returns a tuple of object Player and it's count of moves
        Returns False if there is no winner
        """
        hor = self.check_horizontal()
        ver = self.check_vertical()
        diag_right = self.check_diagonal_right()
        diag_left = self.check_diagonal_left()
        board = self.board().board()
        if hor:
            count = np.count_nonzero(np.char.count(board, hor))
            return self.get_player_by_sign(hor), count
        elif ver:
            count = np.count_nonzero(np.char.count(board, ver))
            return self.get_player_by_sign(ver), count
        elif diag_right:
            count = np.count_nonzero(np.char.count(board, diag_right))
            return self.get_player_by_sign(diag_right), count
        elif diag_left:
            count = np.count_nonzero(np.char.count(board, diag_left))
            return self.get_player_by_sign(diag_left), count
        else:
            return False
