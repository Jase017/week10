# logic.py
import random


class Board:
    def __init__(self):
        self.board = [[None, None, None], [None, None, None], [None, None, None]]

    def print_board(self):
        for row in self.board:
            print(row)

    def get_winner(self):
        for i in range(0, 3):
            if self.board[i][0] is not None and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
            if self.board[0][i] is not None and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        if self.board[1][1] is not None and (self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[2][0] == self.board[1][1] == self.board[0][2]):
            return self.board[1][1]
        return None

    def is_draw(self):
        for row in self.board:
            if None in row:
                return False
        return True


class Player:
    def __init__(self, symbol, move=None):
        self.symbol = symbol
        self.move = move

    def make_move(self, board):
        if self.move:
            x, y = self.move
            if board[x][y] is not None:
                raise ValueError('Invalid move: this position is already occupied.')
            return x, y
        else:
            while True:
                move = input("input row and col (0-2) separated by space or 'q' to quit: ")
                if move.lower() == 'q':
                    return 'q', 'q'
                try:
                    x, y = map(int, move.split())
                    if 0 <= x <= 2 and 0 <= y <= 2 and board[x][y] is None:
                        return x, y
                    else:
                        print('Invalid input, please try again.')
                except ValueError:
                    print('Invalid input, please try again.')


class Bot(Player):
    def make_move(self, board):
        while True:
            x, y = random.randint(0, 2), random.randint(0, 2)
            if board[x][y] is None:
                return x, y
