from .config import WIDTH, HEIGHT
from .errors import ColumnIsFullError, ColumnOutOfRangeError
import numpy as np


class Board:
    """
    Class Board. Uses NumPy to create empty 2D array,
    print it, and insert players signs.
    Contains attributes:

    :param height: height of the board
    :type height: int

    :param width: width of the board
    :type width: int

    :param board: NumPy object of chosen width and height
    :type board: numpy.ndarray
    """
    def __init__(self, array=None):
        if array is not None:
            self._board = array
            self._width = array.shape[1]
            self._height = array.shape[0]
        else:
            self._board = np.full((HEIGHT, WIDTH), ' ')
            self._height = HEIGHT
            self._width = WIDTH

    def height(self):
        return self._height

    def width(self):
        return self._width

    def board(self):
        return self._board

    def __str__(self):
        """
        Prints current state of board
        """
        board_str = ''
        board_str += ('-' * (self.width() * 4 + 1))
        board_str += '\n'
        for row in self.board():
            row_str = ''
            for item in row:
                row_str += (f'| {item} ')
            row_str += '|\n'
            board_str += row_str
        board_str += ('-' * (self.width() * 4 + 1))
        return board_str

    def insert_player_sign(self, column_number, player_sign):
        """
        Inserts chosen sign to chosen column
        Returns True if operation was succesfull
        Raises exceptions if column number is invalid or column is full
        """
        if column_number not in range(1, self.width()+1):
            raise ColumnOutOfRangeError('Column is out of range')
        else:
            chosen_column = self.board()[:, column_number - 1]
            for index, item in enumerate(reversed(chosen_column)):
                if item == ' ':
                    self._board[self.height()-index-1][column_number-1] = player_sign
                    return True
            if ' ' not in chosen_column:
                raise ColumnIsFullError('Column is full')
