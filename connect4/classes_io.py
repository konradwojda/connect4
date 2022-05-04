from .game import Game
from .player import Player
from .bot import Bot
from .score import Score
import json
import numpy as np
from .errors import InvalidDataError


def write_game(games, data):
    """
    Function creates ready-to-write, as a json, games list
    """
    id = 0
    for game in games:
        player1_name = game.players()[0].name()
        player1_sign = game.players()[0].sign()
        player1_is_bot = isinstance(game.players()[0], Bot)
        player2_name = game.players()[1].name()
        player2_sign = game.players()[1].sign()
        player2_is_bot = isinstance(game.players()[1], Bot)
        current_player = game.current_player().name()
        board = game.board().board().tolist()
        game_data = {
            'id': id,
            'player1': {
                'name': player1_name,
                'sign': player1_sign,
                'is_bot': player1_is_bot,
            },
            'player2': {
                'name': player2_name,
                'sign': player2_sign,
                'is_bot': player2_is_bot,
            },
            'current_player': current_player,
            'board': board
        }
        data.append(game_data)
        id += 1
    return data


def write_highscores(highscores, data):
    """
    Function creates ready-to-write, as a json, highscores list
    """
    for score in highscores:
        player_name = score.player_name()
        moves = score.moves()
        score_data = {
            'player_name': player_name,
            'moves': moves
        }
        data.append(score_data)
    return data


def write_to_json(data_to_write, function, file_handle):
    """
    Function writes given data to file handle in json format
    """
    data = []
    data = function(data_to_write, data)
    json.dump(data, file_handle, indent=4)


def read_games(data):
    """
    Function reads games from given data
    Returns list of Game objects
    """
    games = []
    for item in data:
        try:
            id = item['id']
            player1_name = item['player1']['name']
            player1_sign = item['player1']['sign']
            player1_is_bot = item['player1']['is_bot']
            player2_name = item['player2']['name']
            player2_sign = item['player2']['sign']
            player2_is_bot = item['player2']['is_bot']
            current_player_name = item['current_player']
            board = item['board']
            if player1_is_bot:
                player1 = Bot(player1_sign)
            else:
                player1 = Player(player1_name, player1_sign)
            if player2_is_bot:
                player2 = Bot(player2_sign)
            else:
                player2 = Player(player2_name, player2_sign)
            array = np.array(board)
            game = Game([player1, player2], array)
            current_player = game.get_player_by_name(current_player_name)
            game._current_player = current_player
            game._id = id
        except Exception as e:
            raise InvalidDataError from e
        games.append(game)
    return games


def read_highscores(data):
    """
    Function reads scores from given data
    Returns list of Score objects
    """
    highscores = []
    for item in data:
        try:
            player_name = item['player_name']
            moves = item['moves']
            score = Score(player_name, moves)
        except Exception as e:
            raise InvalidDataError from e
        highscores.append(score)
    return highscores


def read_from_json(function, file_handle):
    """
    Uses given read function to read json data from file handle
    """
    data = json.load(file_handle)
    return function(data)
