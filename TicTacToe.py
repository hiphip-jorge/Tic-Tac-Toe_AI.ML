# CS 4375 Project
# This program uses Reinforcement Learning for Game Playing.
# The game is question is Tic-Tac-Toe.
# Game Rules:
# -Getting three in a row of the same 'symbol' wins the game.
# -The AI will always have the 'O' symbol.
# -The Player will always have the 'X' symbol.
# The AI will learn based off of values of the board, and the 2-in-a-row integer feature.
# It will then decide which value on the board to change and be rewarded accordingly.

# import necessary libraries
import numpy as np

BOARD_SIZE = 3
positions = {
    (0, 0): "UPPER LEFT",
    (0, 1): "UPPER MIDDLE",
    (0, 2): "UPPER RIGHT",
    (1, 0): "MIDDLE LEFT",
    (1, 1): "MIDDLE MIDDLE",
    (1, 2): "MIDDLE RIGHT",
    (2, 0): "LOWER LEFT",
    (2, 1): "LOWER MIDDLE",
    (2, 2): "LOWER RIGHT"
}


# core of the program, implements and utilizes User, AI, and Board classes
class TicTacToe:
    def __init__(self, player1, player2):
        # constructor function of TicTacToe class
        # Player 1 (Xs) and Player 2 (Os)
        self.p1_x = player1
        self.p2_o = player2

        # create board
        self.board = Board(self.p1_x, self.p2_o)

        # plays the game n number of times in order to train AI
        # def training_game(self, n):

    # renders the board through TicTacToe class (Probably won't need. Used for testing for now)
    def render_board(self):
        self.board.render()

    # plays the game with each player making a move as normal
    def play_game(self):
        self.board.render()
        # enter a loop that will be broken after n iterations or the users declares a stoppage
        # for testing purposes, 3 games for now
        for i in range(3):
            print("Game " + str(i + 1))
            # iterate through 9 possible moves or break once player has wins, player.game_won  = True
            for j in range(9):
                # first player makes a move
                row, col = self.p1_x.make_a_move()
                # set position on the board
                self.board.set_position(self.p1_x, row, col)
                # if game winning move, set player to game_won == True, and break
                if self.board.check_win():
                    self.p1_x.game_won = True
                    break
                # render updated board
                self.board.render()
                # second player makes a move, if its AI, it makes decision here based off Q-values and reward AI
                row, col = self.p2_o.make_a_move()
                # set position on board
                self.board.set_position(self.p2_o, row, col)
                # if game winning move, set player to game_won == True, and break
                if self.board.check_win():
                    self.p2_o.game_won = True
                    break
                # render updated board
                self.board.render()
                # if game winning move, set player to game_won == True, and break
                self.board.check_win()
                # if there are no more moves possible, game concludes in draw, break loop
            # if player 1 won, award a point (player1.player_wins), then reset player1.game_won = False
            if self.p1_x.game_won:
                self.p1_x.player_wins()
            # if player 2 won, award a point (player2.player_wins), then reset player2.game_won = False
            if self.p2_o.game_won:
                self.p2_o.player_wins()
            # display score
            print("Scoreboard:")
            print(self.p1_x.get_username() + ":" + str(self.p1_x.get_score()))
            print(self.p2_o.get_username() + ":" + str(self.p2_o.get_score()))
            # reset board
            self.board.reset()


# creates the Tic Tac Toe game and runs it for two players
class Board:
    def __init__(self, player1, player2):
        # create symbols assigned to players
        # X=-1, O=1
        self.X = player1
        self.O = player2

        # create array to hold info about board
        self.board_state = np.zeros((BOARD_SIZE, BOARD_SIZE))

    def render(self):
        # create rendering array to store values as symbols to display
        rendering_array = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

        # get values and store into renderingArray as symbols
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board_state[row][col] == -1:
                    rendering_array[row][col] = 'X'
                elif self.board_state[row][col] == 1:
                    rendering_array[row][col] = 'O'

        # print renderingArray in readable and interpretable format
        # this code also enters in a newline character so the next text displayed/entered is on a new line
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in rendering_array]))

    # update board based on player's move decision
    def set_position(self, player, row_pos, col_pos):
        # if player x makes a move, update board positions while checking availability
        if self.X == player and self.board_state[row_pos][col_pos] == 0:
            self.board_state[row_pos][col_pos] = -1
        # if player x makes a move, update board positions while checking availability
        if self.O == player and self.board_state[row_pos][col_pos] == 0:
            self.board_state[row_pos][col_pos] = 1

    # resets board to original state
    def reset(self):
        self.board_state = np.zeros((BOARD_SIZE, BOARD_SIZE))

    # checks board after every set_position(), and resets if win, stating to player if there's a win or not
    def check_win(self):
        # create win state boolean variable, initialize to false
        # change to true if win occurs
        win = False

        # check if win
        # reminder: [rows][columns]
        # check horizontals
        if self.board_state[0][0] == self.board_state[0][1] == self.board_state[0][2] != 0:
            win = True
        if self.board_state[1][0] == self.board_state[1][1] == self.board_state[1][2] != 0:
            win = True
        if self.board_state[2][0] == self.board_state[2][1] == self.board_state[2][2] != 0:
            win = True

        # check verticals
        if self.board_state[0][0] == self.board_state[1][0] == self.board_state[2][0] != 0:
            win = True
        if self.board_state[0][1] == self.board_state[1][1] == self.board_state[2][1] != 0:
            win = True
        if self.board_state[0][2] == self.board_state[1][2] == self.board_state[2][2] != 0:
            win = True

        # check diagonals
        if self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] != 0:
            win = True
        if self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] != 0:
            win = True

        # return win
        return win
# TODO


# to register necessary stuff for User to play the game
class User:
    def __init__(self, name):
        # username: name of player
        # score: player's score
        # game_won: verifies playing status
        self.username = name
        self.score = 0
        self.game_won = False

    def get_username(self):
        return self.username

    def get_score(self):
        return self.score

    def make_a_move(self):
        print(self.username + ", make a move")
        row = input("row?")
        col = input("column?")
        return int(row), int(col)

    def player_wins(self):
        print("\n" + self.username + " wins!!!\n")
        self.score += 1
        self.game_won = False

# TODO


# main function that implements TicTacToe class
def main():
    Bob = User("Bob")
    Jane = User("Jane")
    run = TicTacToe(Bob, Jane)
    run.play_game()


if __name__ == "__main__":
    main()



# end program.