from connect4.database import Database, HighscoresDatabase
from connect4.player import Player
from connect4.game import Game
from connect4.score import Score


def test_database():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    games = [
        Game([player1, player2]),
        Game([player1, player2])
    ]
    db = Database(games)
    assert len(db.games()) == 2
    assert all(game in db.games() for game in games)


def test_database_add_game():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    games = [
        Game([player1, player2]),
        Game([player1, player2])
    ]
    db = Database(games)

    player3 = Player('3', 'l')
    game = Game([player2, player3])
    db.add_game(game)
    assert len(db.games()) == 3
    assert game in db.games()


def test_database_remove_game():
    player1 = Player('1', 'x')
    player2 = Player('2', 'o')
    games = [
        Game([player1, player2]),
        Game([player1, player2])
    ]
    db = Database(games)

    player3 = Player('3', 'l')
    game = Game([player2, player3])
    db.add_game(game)
    assert len(db.games()) == 3
    assert game in db.games()
    db.remove_game(game)
    assert len(db.games()) == 2
    assert all(game in db.games() for game in games)


def test_highscores():
    score1 = Score('1', 5)
    score2 = Score('2', 10)
    db = HighscoresDatabase([score1, score2])
    assert len(db.scores()) == 2


def test_highscores_add_score():
    score1 = Score('1', 5)
    score2 = Score('2', 10)
    db = HighscoresDatabase([score1, score2])
    assert len(db.scores()) == 2
    score3 = Score('3', 7)
    db.add_score(score3)
    assert len(db.scores()) == 3
    assert score3 in db.scores()


def test_highscores_sort_scores():
    score1 = Score('1', 5)
    score2 = Score('2', 10)
    db = HighscoresDatabase([score1, score2])
    assert len(db.scores()) == 2
    score3 = Score('3', 7)
    db.add_score(score3)
    assert len(db.scores()) == 3
    assert score3 in db.scores()
    db.sort_scores()
    assert db.scores()[0] == score1
    assert db.scores()[1] == score3
    assert db.scores()[2] == score2
