# cli.py
import random
import csv
import os
from datetime import datetime
from logic import Board, Player, Bot

class Game:
    def __init__(self, num_of_players='1'):
        symbols = ['X', 'O']
        random.shuffle(symbols)

        self.start_time = datetime.now()
        self.first_move = None
        self.first_player = None  #Record the first move
        self.player1_moves = 0
        self.player2_moves = 0

        if num_of_players == '1':
            self.player1 = Player(symbols[0])
            self.player2 = Bot(symbols[1])
            self.mode = 'Human vs Bot'
        elif num_of_players == '2':
            self.player1 = Player(symbols[0])
            self.player2 = Player(symbols[1])
            self.mode = 'Human vs Human'

        self.board = Board()
        self.current_player = self.player1

    def play(self):
        while not self.board.get_winner() and not self.board.is_draw():
            self.board.print_board()
            print('Next turn: ', self.current_player.symbol)
            x, y = self.current_player.make_move(self.board.board)
            if self.first_move is None:
                self.first_move = x * 3 + y
                self.first_player = self.current_player.symbol  # Record the first player
            if self.current_player == self.player1:
                self.player1_moves += 1
            else:
                self.player2_moves += 1
            if x == 'q' and y == 'q':
                print("Game exited by the player.")
                break
            self.board.board[x][y] = self.current_player.symbol
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2

        winner = self.board.get_winner()

        self.board.print_board()

        if winner:
            print(winner, ' Won')
        elif self.board.is_draw():
            print("It's a draw.")
        self.log_game_data()

    def log_game_data(self):
        if not os.path.exists('log'):
            os.makedirs('log')

        game_id = datetime.now().strftime("%Y%m%d%H%M%S")
        duration = (datetime.now() - self.start_time).seconds

        with open('log/game_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header if the file is empty
            if os.path.getsize('log/game_data.csv') == 0:
                writer.writerow(['Game_ID', 'Mode', 'First_Move', 'Duration', 'First_Player_Outcome', 'Player1_Moves', 'Player2_Moves', 'Winner'])

            winner_symbol = self.board.get_winner()
            first_player_outcome = 'Draw'
            if winner_symbol == self.player1.symbol:
                first_player_outcome = 'Won' if self.first_player == self.player1.symbol else 'Lost'
            elif winner_symbol == self.player2.symbol:
                first_player_outcome = 'Won' if self.first_player == self.player2.symbol else 'Lost'

            writer.writerow([game_id, self.mode, self.first_move, duration, first_player_outcome, self.player1_moves, self.player2_moves, winner_symbol])

if __name__ == '__main__':
    while True:
        num_of_players = input('Enter number of players (1 or 2): ')
        while num_of_players not in ['1', '2']:
            print("Invalid input. Please enter '1' or '2'.")
            num_of_players = input('Enter number of players (1 or 2): ')
        game = Game(num_of_players)
        game.play()
        while True:
            play_again = input('Do you want to play again? (Y/N): ')
            if play_again.upper() == 'Y':
                break
            elif play_again.upper() == 'N':
                exit()
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
