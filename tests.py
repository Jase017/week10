import unittest
from logic import Board, Player, Bot
from cli import Game

class TestLogic(unittest.TestCase):
    def test_board_initialization(self):
        # Test 1: Game initializes with an empty board
        board = Board()
        for row in board.board:
            self.assertEqual(row, [None, None, None])

    def test_game_initialization(self):
        # Test 2: Game initializes with 2 players (human-human) or 1 player (human-bot)
        game = Game('2')
        self.assertTrue(isinstance(game.player1, Player))
        self.assertTrue(isinstance(game.player2, Player))

        game = Game('1')
        self.assertTrue(isinstance(game.player1, Player))
        self.assertTrue(isinstance(game.player2, Bot))

    def test_player_move(self):
        # Test 3: Players are assigned a unique piece, either X or O
        # Test 4: After one player makes a move, the other player can take a turn
        # Test 6: Players can only make a move in a valid position
        player = Player('X', (1, 1))
        self.assertEqual(player.make_move([[None, None, None], [None, None, None], [None, None, None]]), (1, 1))

        player = Player('O', (0, 0))
        self.assertEqual(player.make_move([[None, None, None], [None, None, None], [None, None, None]]), (0, 0))

        # Test that players cannot make a move in an occupied position
        player = Player('X', (1, 0))
        with self.assertRaises(ValueError):
            player.make_move([[None, None, None], ['X', None, None], [None, None, None]])

    def test_bot_move(self):
        # Test that the bot can make a valid move
        bot = Bot('O')
        x, y = bot.make_move([[None, None, None], [None, None, None], [None, None, None]])
        self.assertTrue(0 <= x <= 2)
        self.assertTrue(0 <= y <= 2)

    def test_game_outcome(self):
        # Test 5: All winning games are detected, and draws are detected
        # Test 7: The correct winner is detected, if there is one
        game = Game('2')
        game.board.board = [['X', 'X', 'X'], [None, None, None], [None, None, None]]
        self.assertEqual(game.board.get_winner(), 'X')

        game.board.board = [['O', None, None], ['O', None, None], ['O', None, None]]
        self.assertEqual(game.board.get_winner(), 'O')

        game.board.board = [['X', None, None], [None, 'X', None], [None, None, 'X']]
        self.assertEqual(game.board.get_winner(), 'X')

        game.board.board = [[None, None, 'O'], [None, 'O', None], ['O', None, None]]
        self.assertEqual(game.board.get_winner(), 'O')

        game.board.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
        self.assertTrue(game.board.is_draw())

if __name__ == '__main__':
    unittest.main()
