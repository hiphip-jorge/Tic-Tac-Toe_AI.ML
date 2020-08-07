#CS 4375 Project
#This program uses Reinforcement Learning for Game Playing.
#The game is question is Tic-Tac-Toe.
#Game Rules:
# -Getting three in a row of the same 'symbol' wins the game.
# -The AI will always have the 'O' symbol.
# -The Player will always have the 'X' symbol.
#The AI will learn based off of values of the board, and the 2-in-a-row integer feature. It will then decide which value on the board to change and be rewarded accordingly.

#import necessary libraries
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
        # attributes of TicTacToe class
        # p1_x: player 1 (Xs), p2_o: player 2 (Os)
        # board: tic-tac-toe board (Board class)
        # is_ai_x/o: checks if Player is of AI class (bool)
        self.p1_x = player1
        self.p2_o = player2
        self.board = Board(self.p1_x, self.p2_o)
        self.is_ai_x = isinstance(player1, AI)
        self.is_ai_o = isinstance(player2, AI)

    # plays the game with each player making a move as normal
    def play_game(self):
        # enter a loop that will be broken after n iterations or the users declares a stoppage
        # for testing purposes, 3 games for now
        for i in range(3):
            print("Game " + str(i + 1))
            # iterate through 9 possible moves or break once player has wins, player.game_won  = True
            while True:
                # input boolean (user only)
                valid_input = False
                # first player makes a move
                if self.is_ai_x:
                    row, col = self.p1_x.takeTurn(self.board.get_avail(), self.board.get_board_state(), 1)
                else:
                    while not valid_input:
                        row, col = self.p1_x.make_a_move()
                        valid_input = self.valid_input(row, col)
                        if not valid_input:
                            print("\nRow " + str(row) + " and column " + str(col) + " is not an available move. "
                                                                           "Try again.\n")
                # set position on the board
                self.board.set_position(self.p1_x, row, col)
                # reset valid_input to false for player2
                valid_input = False
                # if game winning move, set player to game_won == True, and break
                if self.board.check_win():
                    self.p1_x.game_won = True
                    break
                # check for draw
                if len(self.board.get_avail()) == 0:
                    print("\nDraw! No winner!")
                    break
                # render updated board
                self.board.render()
                # second player makes a move, if its AI, it makes decision here based off Q-values and reward AI
                if self.is_ai_o:
                    row, col = self.p2_o.takeTurn(self.board.get_avail(), self.board.get_board_state(), -1)
                else:
                    while not valid_input:
                        row, col = self.p2_o.make_a_move()
                        valid_input = self.valid_input(row, col)
                        if not valid_input:
                            print("\nRow " + str(row) + " and column " + str(col) + " is not an available move. "
                                                                           "Try again.\n")
                # set position on board
                self.board.set_position(self.p2_o, row, col)
                # if game winning move, set player to game_won == True, and break
                if self.board.check_win():
                    self.p2_o.game_won = True
                    break
                # render updated board
                self.board.render()
                print()
                # if game winning move, set player to game_won == True, and break
                self.board.check_win()
                # if there are no more moves possible, game concludes in draw, break loop
            # if player 1 won, award a point (player1.player_wins), then reset player1.game_won = False
            if self.p1_x.game_won:
                self.p1_x.player_wins()
            # if player 2 won, award a point (player2.player_wins), then reset player2.game_won = False
            if self.p2_o.game_won:
                self.p2_o.player_wins()
            # render winning board
            self.board.render()
            print()
            # display score
            print("Scoreboard:")
            print(self.p1_x.get_username() + ": " + str(self.p1_x.get_score()))
            print(self.p2_o.get_username() + ": " + str(self.p2_o.get_score()) + "\n")
            # reset board
            self.board.reset()

    # plays the game x number of times in order to train AI
    def training_game(self, x):
        # train the AI x number of times
        for n in range(x):
            # print loading screen.
            if (n % 100) == 0:
                print("Loading {}%".format(100*(n/x)))
            # perform game while checking if game is over
            while self.gameIsOver() != True:
                # get position of board
                available_positions = self.board.get_avail()

                # get action for p1_x
                action_player1_row, action_player1_col = self.p1_x.takeTurn(available_positions, self.board.board_state, -1)

                # perform the action and update the board accordingly for future moves.
                self.board.set_position(self.p1_x, action_player1_row, action_player1_col)

                # append the board for the player to reflect the decision
                hash_of_board = self.board.getHashOfBoard()
                self.p1_x.appendHashOfBoard(hash_of_board)

                # check if move won the game
                win_state = self.board.check_win()

                if win_state == True:
                    # game has ended, set rewards to AI's
                    self.rewardTTT(self.p1_x, self.p2_o)

                    # reset everything
                    self.p1_x.reset()
                    self.p2_o.reset()
                    self.board.reset()

                    break
                elif self.gameIsOver() != True:
                    # get position of board
                    available_positions = self.board.get_avail()

                    # get action for p2_o
                    action_player2_row, action_player2_col = self.p2_o.takeTurn(available_positions, self.board.board_state, 1)

                    # perform the action and update the board accordingly for future moves.
                    self.board.set_position(self.p2_o, action_player2_row, action_player2_col)

                    # append the board for the player to reflect the decision
                    hash_of_board = self.board.getHashOfBoard()
                    self.p2_o.appendHashOfBoard(hash_of_board)

                    # check if move won the game
                    win_state = self.board.check_win()

                    if win_state == True:
                        # game has ended, set rewards to AI's
                        self.rewardTTT(self.p2_o, self.p1_x)

                        # reset everything
                        self.p1_x.reset()
                        self.p2_o.reset()
                        self.board.reset()

                        break

    # checks if game is over
    def gameIsOver(self):
        if self.board.check_win:
            return True
        elif len(self.board.get_avail()) == 0:
            return True
        else:
            return False

    # validate player move is available and acceptable
    def valid_input(self, row, col):
        # verify in bounds
        if row < 0 or col < 0 or row > 2 or col > 2:
            return False
        # take in player move
        move = (row, col)
        # verify player move is available on board
        return move in self.board.get_avail()

    # gives reward to AI based on decisions of board
    # winner and loser are AI objects
    def rewardTTT(self, winner, loser):
        # get result BEFORE board is reset
        isWin = self.board.check_win()
        # give reward through back-propagation
        if isWin:
            winner.rewardAI(1)
            loser.rewardAI(0)
        else:
            winner.rewardAI(0.2)
            loser.rewardAI(0.2)


# creates the Tic Tac Toe game and runs it for two players
class Board:
    def __init__(self, player1=-1, player2=1):
        # create symbols assigned to players
        # X=-1, O=1
        self.X = player1
        self.O = player2

        # create array to hold info about board
        self.board_state = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.board_hash = None

    def render(self):
        # create rendering array to store values as symbols to display
        rendering_array = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]

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
        if self.X == player:
            self.board_state[row_pos][col_pos] = -1
        # if player o makes a move, update board positions while checking availability
        if self.O == player:
            self.board_state[row_pos][col_pos] = 1

    # returns board_state
    def get_board_state(self):
        return self.board_state

    # Provides a list of available moves for the AI
    def get_avail(self):
        # pos_list: the returning list with the available positions on the board
        pos_list = []
        # iterate through the whole board, appending the available spots to pos_list
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # if spot is not occupied, append
                if self.board_state[i, j] == 0:
                    # the positions dictionary is used to hash the available spot to the list
                    pos_list.append((i, j))
        return pos_list

    # resets board to original state
    def reset(self):
        self.board_state = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.board_hash = None

    # checks board after every set_position(), and resets if win, stating to player if theres a win or not
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

    # get hash of board
    def getHashOfBoard(self):
        totalPositions = (BOARD_SIZE * BOARD_SIZE)
        self.board_hash = str(self.board_state.reshape(totalPositions))
        return self.board_hash

# an AI for the user to go against, epsilon is nonzero when training, zero when trained so no more training occurs.
class AI:
    def __init__(self, name):
        # assign necessary variables
        # experimentation needed to refine variables for optimal AI training
        # epsilon is changeable by main
        self.learningRate = .5
        self.decayRate = .5
        self.epsilon = .5

        # create necessary variables for AI to record and alter data.
        self.name = name
        self.board_state = []
        self.board_state_q = {}

        self.score = 0
        self.game_won = False
        self.turn = [(0,0)]

    # make the AI take its turn, random if untrained.
    # player_symbol will be equal to 1 or -1
    def takeTurn(self, board_available_positions, board_state, player_symbol):
        # Prompt AI for move
        print("AI's move")
        #for initializion, use uniform random experimentation
        if np.random.uniform(0,1) < self.epsilon:
            #fill in random square on the board from available positions
            self.turn = board_available_positions[np.random.choice(len(board_available_positions))]
        else:
            # set min value for AI to view as lowest acceptable position.
            min = -999

            # iterate through all available board positions
            for pos in board_available_positions:
                # copy board state to modify without changing original board state
                next_board_state = board_state.copy()
                # set symbol at position of board, changing board state
                next_board_state[pos] = player_symbol
                # get hash of new board state
                next_board_state_hash = self.getHashOfBoard(next_board_state)
                # create trueValue to grow as board states progress, set to zero after last board state is hashed
                trueValue = 0 if self.board_state_q.get(next_board_state_hash) is None else self.board_state_q.get(next_board_state_hash)
                # determine if pos is best move based on trueValue
                if trueValue >= min:
                    min = trueValue
                    self.turn = pos
        # return AI's decision (turn)
        return self.turn[0], self.turn[1]

    # get hash of board
    def getHashOfBoard(self, boardState):
        totalPositions = (BOARD_SIZE * BOARD_SIZE)
        hash = str(boardState.reshape(totalPositions))
        return hash

    # append hash of board
    def appendHashOfBoard(self, boardState):
        self.board_state.append(boardState)

    # after every game, update board_state_value through back-propagation to learn from previous game
    def rewardAI(self, rewardValue):
        for state in reversed(self.board_state):
            # check if learned values is empty, meaning first game.
            if self.board_state_q.get(state) is None:
                #initiliaze to zero at state location
                self.board_state_q[state] = 0
            # use q-learning formula and constants to update state table
            self.board_state_q[state] += self.learningRate * (self.decayRate * rewardValue - self.board_state_q[state])
            # utilize backpropogation for next state behind current state.
            rewardValue = self.board_state_q[state]

    # after every game, reset board_state to prepare for next game
    def reset(self):
        self.board_state = []

    def player_wins(self):
        print("\n" + self.name + " wins!!!")
        self.score += 1
        self.game_won = False

    def get_username(self):
        return self.name

    def get_score(self):
        return self.score

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
        row = input("row: ")
        col = input("column: ")
        return int(row), int(col)

    def player_wins(self):
        print("\n" + self.username + " wins!!!\n")
        self.score += 1
        self.game_won = False


# main function that implements TicTacToe class
if __name__ == "__main__":
    # create variable to allow user to play again, initiliaze to True
    play_again = True

    # train AI
    # create AI objects for training
    player1 = AI("Player 1")
    player2 = AI("Player 2")

    # create TicTacToe object to train AI
    run = TicTacToe(player1, player2)

    # set epochs (iterations) to 10,000 and run.
    run.training_game(10000)

    #set player2 to be User
    userName = input("Please enter your name: ")
    player2 = User(userName)

    # Create AI vs User instance of TicTacToe object
    run = TicTacToe(player1, player2)

    # ask if user wants to play again based on binary state of playAgain value
    while play_again:
        run.play_game()
        player_choice = input("Type '1' to play again, and anyything else to end the program: ")
        if player_choice != '1':
            play_again = False

  #end program.
