from connect4.player import Player
from connect4.classes_io import (write_game, write_highscores, write_to_json,
                                 read_highscores, read_games, read_from_json)
from connect4.database import Database, HighscoresDatabase


def test_read_from_json():
    with open('tests/test_classes_io_read.json', 'r') as handle:
        games = read_from_json(read_games, handle)
    db = Database(games)
    assert db.get_game_by_id(0).players()[0].name() == 'konrad'
    assert isinstance(db.get_game_by_id(0).players()[0], Player) is True
    assert db.get_game_by_id(0).players()[1].name() == 'maciej'
    assert isinstance(db.get_game_by_id(0).players()[1], Player) is True
    assert db.get_game_by_id(0).players()[0].sign() == 'x'
    assert db.get_game_by_id(0).players()[1].sign() == 'o'
    assert db.get_game_by_id(0).board().board().shape == (6, 7)


def test_write_to_json():
    with open('tests/test_classes_io_read.json', 'r') as handle:
        games = read_from_json(read_games, handle)
    db = Database(games)
    assert db.get_game_by_id(0).players()[0].name() == 'konrad'
    assert db.get_game_by_id(0).players()[1].name() == 'maciej'
    assert db.get_game_by_id(0).players()[0].sign() == 'x'
    assert db.get_game_by_id(0).players()[1].sign() == 'o'
    assert isinstance(db.get_game_by_id(0).players()[0], Player) is True
    assert isinstance(db.get_game_by_id(0).players()[1], Player) is True
    assert db.get_game_by_id(0).board().board().shape == (6, 7)
    with open('tests/test_classes_io_write.json', 'w') as handle:
        write_to_json(games, write_game, handle)
    with open('tests/test_classes_io_write.json', 'r') as handle:
        games = read_from_json(read_games, handle)
    db = Database(games)
    assert db.get_game_by_id(0).players()[0].name() == 'konrad'
    assert db.get_game_by_id(0).players()[1].name() == 'maciej'
    assert db.get_game_by_id(0).players()[0].sign() == 'x'
    assert db.get_game_by_id(0).players()[1].sign() == 'o'
    assert isinstance(db.get_game_by_id(0).players()[0], Player) is True
    assert isinstance(db.get_game_by_id(0).players()[1], Player) is True
    assert db.get_game_by_id(0).board().board().shape == (6, 7)


def test_read_highscores_from_json():
    with open('tests/test_highscores_read.json', 'r') as handle:
        scores = read_from_json(read_highscores, handle)
    hdb = HighscoresDatabase(scores)
    assert hdb.scores()[0].player_name() == 'konrad'
    assert hdb.scores()[0].moves() == 4
    assert hdb.scores()[1].player_name() == 'konrad'
    assert hdb.scores()[1].moves() == 6
    assert hdb.scores()[2].player_name() == 'Basia'
    assert hdb.scores()[2].moves() == 7
    assert hdb.scores()[3].player_name() == 'Konrad'
    assert hdb.scores()[3].moves() == 10


def test_write_highscores_to_json():
    with open('tests/test_highscores_read.json', 'r') as handle:
        scores = read_from_json(read_highscores, handle)
    with open('tests/test_highscores_write.json', 'w') as handle:
        write_to_json(scores, write_highscores, handle)
    with open('tests/test_highscores_write.json', 'r') as handle:
        scores = read_from_json(read_highscores, handle)
    hdb = HighscoresDatabase(scores)
    assert hdb.scores()[0].player_name() == 'konrad'
    assert hdb.scores()[0].moves() == 4
    assert hdb.scores()[1].player_name() == 'konrad'
    assert hdb.scores()[1].moves() == 6
    assert hdb.scores()[2].player_name() == 'Basia'
    assert hdb.scores()[2].moves() == 7
    assert hdb.scores()[3].player_name() == 'Konrad'
    assert hdb.scores()[3].moves() == 10


