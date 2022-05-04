from connect4.player import Player
from connect4.bot import Bot
from connect4.game import Game
from connect4.board import Board
from connect4.score import Score
from connect4.errors import (InvalidNameError, InvalidPlayerCount,
                             ColumnIsFullError, ColumnOutOfRangeError)
from connect4.config import HEIGHT, WIDTH
import random
import pytest


def test_player_create():
    player = Player('konrad', 'x')
    assert player.name() == 'konrad'
    assert player.sign() == 'x'


def test_player_create_empty_name():
    with pytest.raises(InvalidNameError):
        Player('', 'x')


def test_bot_create():
    bot = Bot('o')
    assert bot.sign() == 'o'


def test_board_create():
    board = Board()
    assert board.height() == HEIGHT
    assert board.width() == WIDTH
    assert board.board().shape == (HEIGHT, WIDTH)


def test_board_insert_player_sign_normal():
    board = Board()
    board.insert_player_sign(3, 'x')
    assert board.insert_player_sign(3, 'x') is True
    assert board.board()[HEIGHT-1][2] == 'x'


def test_board_insert_player_sign_invalid_col():
    board = Board()
    with pytest.raises(ColumnOutOfRangeError):
        board.insert_player_sign(8, 'o')


def test_board_insert_player_sign_full_column():
    board = Board()
    for _ in range(6):
        board.insert_player_sign(3, 'x')
    with pytest.raises(ColumnIsFullError):
        board.insert_player_sign(3, 'x')


def test_game_create():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    assert game.players() == [player1, player2]
    assert game.height() == HEIGHT
    assert game.width() == WIDTH
    assert game.board().board().shape == (HEIGHT, WIDTH)
    assert game.current_player() is None
    assert game.id() is None


def test_game_create_invalid_players_list():
    player1 = Player('1', 'x')
    with pytest.raises(InvalidPlayerCount):
        Game([player1, player1, player1])


def test_game_choose_first_player(monkeypatch):
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])

    def first_player(list):
        return player1

    monkeypatch.setattr(random, "choice", first_player)
    game.choose_first_player()
    assert game.current_player() == player1


def test_get_player_name_by_sign():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    assert game.get_player_by_sign('o') == player2


def test_get_player_name_by_name():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    assert game.get_player_by_name('2') == player2


def test_toggle():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game._current_player = player1
    game.toggle()
    assert game.current_player() == player2


def test_check_horizontal_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'x')
    game.board().insert_player_sign(2, 'x')
    game.board().insert_player_sign(3, 'x')
    game.board().insert_player_sign(4, 'x')
    assert game.check_horizontal() == 'x'


def test_check_vertical_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    for _ in range(4):
        game.board().insert_player_sign(3, 'x')
    assert game.check_vertical() == 'x'


def test_check_horizontal_no_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'x')
    assert game.check_horizontal() is False


def test_check_vertical_no_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(3, 'x')
    assert game.check_vertical() is False


def test_check_diagonal_right_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'x')
    game.board().insert_player_sign(2, 'o')
    game.board().insert_player_sign(2, 'x')
    game.board().insert_player_sign(3, 'o')
    game.board().insert_player_sign(3, 'o')
    game.board().insert_player_sign(3, 'x')
    game.board().insert_player_sign(4, 'o')
    game.board().insert_player_sign(4, 'o')
    game.board().insert_player_sign(4, 'o')
    game.board().insert_player_sign(4, 'x')
    assert game.check_diagonal_right() == 'x'


def test_check_diagonal_left_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'x')
    game.board().insert_player_sign(2, 'o')
    game.board().insert_player_sign(2, 'o')
    game.board().insert_player_sign(2, 'x')
    game.board().insert_player_sign(3, 'o')
    game.board().insert_player_sign(3, 'x')
    game.board().insert_player_sign(4, 'x')
    assert game.check_diagonal_left() == 'x'


def test_check_diagonal_right_no_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'x')
    assert game.check_diagonal_right() is False


def test_check_diagonal_left_no_win():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'x')
    assert game.check_diagonal_left() is False


def test_check_winner():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    game = Game([player1, player2])
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'o')
    game.board().insert_player_sign(1, 'x')
    game.board().insert_player_sign(2, 'o')
    game.board().insert_player_sign(2, 'o')
    game.board().insert_player_sign(2, 'x')
    game.board().insert_player_sign(3, 'o')
    game.board().insert_player_sign(3, 'x')
    game.board().insert_player_sign(4, 'x')
    assert game.check_winner() == (player1, 4)


def test_score_create():
    player = 'nazwa'
    moves = 5
    score = Score(player, moves)
    assert score.moves() == 5
    assert score.player_name() == 'nazwa'


def test_score_str():
    player = 'nazwa'
    moves = 5
    score = Score(player, moves)
    assert score.moves() == 5
    assert score.player_name() == 'nazwa'
    assert str(score) == 'Winner: nazwa, Moves count: 5'
