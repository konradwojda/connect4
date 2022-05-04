from .player import Player
from .game import Game
from .bot import Bot
from .score import Score
from .database import Database, HighscoresDatabase
from .errors import (DatabasePathNotFound, FileIsEmptyError,
                     ColumnIsFullError, ColumnOutOfRangeError)
import numpy as np
import sys


class Interface:
    """
    Class Interface. Contains attributes:

    :param game: current game
    :type game: Game
    """
    def __init__(self, game=None):
        self._game = game

    def game(self):
        return self._game

    def _greet(self):
        message = 'Welcome to Connect4 game'
        print('-' * len(message))
        print(message)
        print('-' * len(message))

    def _print_options(self):
        print("")
        print("1. Start PvP game")
        print("2. Start PvB game")
        print("3. Load a game from database")
        print("4. Delete a game from database")
        print("5. View highscores")
        print("6. Exit")
        print("")

    def _get_choice(self):
        choice = input("Choose an option: \n")
        return choice

    def _get_column(self):
        msg = 'Type \'save\' to save game\nChoose column to put your sign in:\n'
        choice = input(msg)
        return choice

    def _get_game_id(self):
        id = input("Choose game id: \n")
        return id

    def _get_player_name(self):
        player_name = input("Enter your name: \n")
        while not player_name.strip():
            print('Name cannot be blank or empty')
            player_name = input("Enter your name: \n")
        return player_name

    def _get_sign(self):
        sign = input("Input your sign: \n")
        while not sign.strip() or len(sign.strip()) > 1:
            if not sign.strip():
                print('Sign cannot be blank or empty')
            if len(sign.strip()) > 1:
                print('Sign length has to be 1')
            sign = input("Input your sign: \n")
        return sign

    def _get_bot_sign(self):
        sign = input("Input bot\'s sign: \n")
        while not sign.strip() or len(sign.strip()) > 1:
            if not sign.strip():
                print('Sign cannot be blank or empty')
            if len(sign.strip()) > 1:
                print('Sign length has to be 1')
            sign = input("Input bot\'s sign: \n")
        return sign

    def create_pvp_game(self):
        """
        Creates a pvp game using players' inputs
        returns Game class object
        """
        players = []
        player1_name = ''
        player2_name = ''
        player1_sign = ''
        player2_sign = ''
        print('*** First player ***')
        player1_name = self._get_player_name()
        player1_sign = self._get_sign()
        print('*** Second player ***')
        player2_name = self._get_player_name()
        while player2_name.strip() == player1_name.strip():
            print('Players\' names cannot be the same')
            player2_name = self._get_player_name()
        player2_sign = self._get_sign()
        while player2_sign.strip() == player1_sign.strip():
            print('Players\' signs cannot be the same')
            player2_sign = self._get_sign()
        players = [Player(player1_name, player1_sign.strip()),
                   Player(player2_name, player2_sign.strip())]
        game = Game(players)
        game.choose_first_player()
        return game

    def create_pvb_game(self):
        """
        Creates a pvb game using players' inputs
        returns Game class object
        """
        print("*** Player ***")
        name = self._get_player_name()
        sign = self._get_sign()
        print("*** Bot ***")
        bot_sign = self._get_bot_sign()
        while bot_sign.strip() == sign.strip():
            print('Bot and player\'s signs cannot be the same')
            bot_sign = self._get_bot_sign()
        player = Player(name, sign.strip())
        bot = Bot(bot_sign.strip())
        game = Game([player, bot])
        game.choose_first_player()
        return game

    def play_pvp(self):
        """
        Starts a player versus player. Creates new game or starts loaded game.
        Returns tuple of player and moves count if there is a winner
        Returns None if there is no winner
        """
        if self.game() is None:
            self._game = self.create_pvp_game()
        board = self.game().board()
        winner = False
        while not winner:
            current_player = self.game().current_player()
            print(str(board))
            print(f'It is {current_player.name()} turn')
            correct_choice = False
            while not correct_choice:
                choice = self._get_column()
                if choice == 'save':
                    correct_choice = True
                    self.save_game()
                    print('Game has been saved')
                    return None
                    break
                else:
                    if not choice.isdigit():
                        print('Please insert a digit')
                        continue
                    try:
                        choice = int(choice)
                        board.insert_player_sign(choice, current_player.sign())
                        correct_choice = True
                    except ColumnOutOfRangeError as e:
                        print(str(e))
                    except ColumnIsFullError as e:
                        print(str(e))
            self.game().toggle()
            winner = self.game().check_winner()
            if np.count_nonzero(np.char.count(board.board(), ' ')) == 0:
                print(str(board))
                return None
                break
        print(str(board))
        return winner

    def play_pvb(self):
        """
        Starts a player versus bot. Creates new game or starts loaded game.
        Returns tuple of player/bot and moves count if there is a winner
        Returns None if there is no winner
        """
        if self.game() is None:
            self._game = self.create_pvb_game()
        board = self.game().board()
        winner = False
        while not winner:
            current_player = self.game().current_player()
            print(str(board))
            if isinstance(current_player, Bot):
                print('It\'s bot\'s turn')
                width = self.game().width()
                column = self.game().current_player().choose_column(width)
                board.insert_player_sign(column, current_player.sign())
            else:
                print('It\'s your turn')
                correct_choice = False
                while not correct_choice:
                    choice = self._get_column()
                    if choice == 'save':
                        correct_choice = True
                        self.save_game()
                        print('Game has been saved')
                        return None
                        break
                    else:
                        if not choice.isdigit():
                            print('Please insert a digit')
                            continue
                        try:
                            choice = int(choice)
                            board.insert_player_sign(choice, current_player.sign())
                            correct_choice = True
                        except ColumnOutOfRangeError as e:
                            print(str(e))
                        except ColumnIsFullError as e:
                            print(str(e))
            self.game().toggle()
            winner = self.game().check_winner()
            if np.count_nonzero(np.char.count(board.board(), ' ')) == 0:
                print(str(board))
                return None
                break
        print(str(board))
        return winner

    def save_game(self):
        """
        Saves game to database file named 'database.json'
        """
        db = Database()
        try:
            db.read_from_file('database.json')
        except DatabasePathNotFound:
            pass
        except FileIsEmptyError:
            pass
        if self.game().id() is None:
            db.add_game(self.game())
            db.save_to_file('database.json')
        else:
            db.remove_game(db.get_game_by_id(self.game().id()))
            db.add_game(self.game())
            db.save_to_file('database.json')

    def load_game(self):
        """
        Loads game from database named 'database.json'
        returns game object
        """
        try:
            db = Database()
            db.read_from_file('database.json')
            db.print_saved_games()
            id = self._get_game_id()
            id = int(id)
            game = db.get_game_by_id(id)
            return game
        except DatabasePathNotFound:
            print('No games to load from database')
            return None
        except FileIsEmptyError:
            print('No games to load from database')
            return None

    def delete_game(self):
        """
        Deletes a game, chosen by user, from database
        """
        try:
            db = Database()
            db.read_from_file('database.json')
            db.print_saved_games()
            id = self._get_game_id()
            id = int(id)
            game = db.get_game_by_id(id)
            db.remove_game(game)
            if len(db.games()) == 0:
                with open('database.json', 'w'):
                    pass
            else:
                db.save_to_file('database.json')
            print('Game has been removed')
        except DatabasePathNotFound:
            print('No games to load from database')
        except FileIsEmptyError:
            print('No games to load from database')

    def view_highscores(self):
        """
        Show highscores saved in file
        """
        try:
            highscores = HighscoresDatabase()
            highscores.read_from_file('highscores.json')
        except FileNotFoundError:
            print('No highscores found')
        except FileIsEmptyError:
            print('No highscores found')
        for score in highscores.scores():
            print(score)

    def load_highscores(self):
        """
        Load highscores to database.
        Returns HighscoresDatabase object
        """
        try:
            highscores = HighscoresDatabase()
            highscores.read_from_file('highscores.json')
        except FileNotFoundError:
            pass
        except FileIsEmptyError:
            pass
        return highscores

    def add_score(self, score):
        """
        Adds score to database
        """
        try:
            highscores = HighscoresDatabase()
            highscores.read_from_file('highscores.json')
        except FileNotFoundError:
            pass
        except FileIsEmptyError:
            pass
        highscores.add_score(score)
        highscores.save_to_file('highscores.json')

    def play(self):
        """
        Prints menu and does chosen action
        1. Starts pvp game with possibility to save it.
        When game ends with winner,
        saves a new score to highscores file named 'highscores.json'
        2. Starts pvb game with possibility to save it.
        3. Loads game from database and starts it. When game ends with winner,
        saves a new score to highscores (only PvP). When you save loaded game
        it overwrites it.
        4. Gives a possiblity to delete saved game from database
        5. Prints highscores from highscores file named 'highscores.json'
        6. Closes game
        """
        self._greet()
        exit = False
        while not exit:
            self._print_options()
            choice = self._get_choice()
            if choice == '1':
                result = self.play_pvp()
                if result is None:
                    print('There is no winner')
                    exit = True
                else:
                    winner, count = result
                    score = Score(winner.name(), count)
                    self.add_score(score)
                    print(f'Winner is {winner.name()} with {count} moves')
                    exit = True
            if choice == '2':
                result = self.play_pvb()
                if result is None:
                    print('There is no winner')
                    exit = True
                else:
                    winner, count = result
                    print(f'Winner is {winner.name()} with {count} moves')
                    exit = True
            if choice == '3':
                game = self.load_game()
                if game:
                    self._game = game
                else:
                    continue
                players = self.game().players()
                if isinstance(players[0], Bot) or isinstance(players[1], Bot):
                    result = self.play_pvb()
                    if result is None:
                        print('There is no winner')
                        exit = True
                    else:
                        winner, count = result
                        print(f'Winner is {winner.name()} with {count} moves')
                        exit = True
                else:
                    result = self.play_pvp()
                    if result is None:
                        print('There is no winner')
                        exit = True
                    else:
                        winner, count = result
                        score = Score(winner.name(), count)
                        self.add_score(score)
                        print(f'Winner is {winner.name()} with {count} moves')
                        exit = True
            if choice == '4':
                self.delete_game()
            if choice == '5':
                self.view_highscores()
            if choice == '6':
                sys.exit()
