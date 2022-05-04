from .game import Game
from .score import Score
from .errors import (
    DatabasePathIsDirectory,
    DatabasePathNotFound,
    DatabasePermissionError,
    FileIsEmptyError
)
from .classes_io import (write_game, write_highscores, write_to_json,
                         read_games, read_highscores, read_from_json)


class DatabaseObject:
    def save_to_file(self, path, data):
        """
        Writes data from database to file
        """
        try:
            with open(path, 'w') as file_handle:
                self._write(data, file_handle)
        except FileNotFoundError:
            raise DatabasePathNotFound("Invalid path")
        except PermissionError:
            raise DatabasePermissionError("No permission to open database")
        except IsADirectoryError:
            raise DatabasePathIsDirectory("This path is a directory")

    def read_from_file(self, path):
        """
        Reads data from file
        """
        try:
            with open(path, 'r') as file_handle:
                file_handle.seek(0)
                first_char = file_handle.read(1)
                if not first_char:
                    raise FileIsEmptyError
            with open(path, 'r') as file_handle:
                return self._read(file_handle)

        except FileNotFoundError:
            raise DatabasePathNotFound("Invalid path")
        except PermissionError:
            raise DatabasePermissionError("No permission to open database")
        except IsADirectoryError:
            raise DatabasePathIsDirectory("This path is a directory")


class Database(DatabaseObject):
    """
    Class Database. Contains attributes:

    :param games: list of games in database
    :type games: list
    """
    def __init__(self, games=None):
        self._games = games if games else []

    def games(self):
        return self._games

    def add_game(self, game: Game):
        """
        Adds game to database
        """
        self.games().append(game)

    def remove_game(self, game):
        """
        Removes game from database
        """
        if game in self.games():
            self.games().remove(game)
            return True
        else:
            raise ValueError('Cannot find game in games list')

    def get_game_by_id(self, id):
        """
        returns game of given id
        returns False if given id is invalid
        """
        for game in self.games():
            if game.id() == id:
                return game
        return False

    def print_saved_games(self):
        """
        Prints games in database
        """
        print('Saved games:')
        for game in self.games():
            id = game.id()
            player1 = game.players()[0]
            player2 = game.players()[1]
            print(f'{id} : {player1.name()} vs {player2.name()}')
        return

    def _read(self, file_handle):
        return read_from_json(read_games, file_handle)

    def _write(self, data, file_handle):
        write_to_json(data, write_game, file_handle)

    def save_to_file(self, path):
        super().save_to_file(path, self.games())

    def read_from_file(self, path):
        self._games = super().read_from_file(path)


class HighscoresDatabase(DatabaseObject):
    """
    Class HighscoresDatabase. Contains attributes:

    :param scores: list of players' scores
    :type scores: list
    """
    def __init__(self, scores=None):
        self._scores = scores if scores else []

    def scores(self):
        return self._scores

    def add_score(self, score: Score):
        """
        Adds score to scores list
        """
        self.scores().append(score)

    def sort_scores(self):
        """
        Sorts scores
        """
        self._scores.sort(key=lambda score: score.moves())

    def save_to_file(self, path):
        self.sort_scores()
        super().save_to_file(path, self.scores())

    def read_from_file(self, path):
        self._scores = super().read_from_file(path)

    def _read(self, file_handle):
        return read_from_json(read_highscores, file_handle)

    def _write(self, data, file_handle):
        write_to_json(data, write_highscores, file_handle)
