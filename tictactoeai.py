# -*- coding: utf-8 -*-
"""TicTacToeAI

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/105LYTpQ-oOqtm0b0VgGBZomeEqshfWE3

# Tic Tac Toe Self learning AI

ref: https://www.kaggle.com/code/dhanushkishore/a-self-learning-tic-tac-toe-program/notebook
"""

# !gdown 1fPh7kQsrev0yQ1T0GN8e4Sw2wde6D13i

from tensorflow import keras
# Importing required moduless
import numpy as np 
#import pandas as pd 
# import pprint,random

model_path = "./TicTacToeModel.h5"

"""# TicTacToe Game Class"""

class tic_tac_toe_game(object):
    def __init__(self):
        self.board=np.full((3,3),2)

    def toss(self):
        """Function to simulate a toss and decide which player goes first

        Args:

        Returns:
        Returns 1 if player assigned mark 1 has won, or 0 if his opponent won

        """
        turn=np.random.randint(0,2,size=1)
        if turn.mean()==0:
            self.turn_monitor=0
        elif turn.mean()==1:
            self.turn_monitor=1
        return self.turn_monitor

    def move(self,player,coord):
        """Function to perform the action of placing a mark on the tic tac toe board
        After performing the action, this function flips the value of the turn_monitor to 
        the next player

        Args:
        player: 1 if player who is assigned the mark 1 is performing the action, 
        0 if his opponent is performing the action
        coord: The coordinate where the 1 or 0 is to be placed on the 
        tic-tac-toe board (numpy array)

        Returns:
        game_status(): Calls the game status function and returns its value
        board: Returns the new board state after making the move

        """
        if self.board[coord]!=2 or self.game_status()!="In Progress" or self.turn_monitor!=player:
            raise ValueError("Invalid move")
        self.board[coord]=player
        self.turn_monitor=1-player
        return self.game_status(),self.board


    def game_status(self):
        """Function to check the current status of the game, 
        whether the game has been won, drawn or is in progress

        Args:

        Returns:
        "Won" if the game has been won, "Drawn" if the 
        game has been drawn, or "In Progress", if the game is still in progress

        """
        #check for a win along rows
        for i in range(self.board.shape[0]):
            if 2 not in self.board[i,:] and len(set(self.board[i,:]))==1:
                return "Won"
        #check for a win along columns
        for j in range(self.board.shape[1]):
            if 2 not in self.board[:,j] and len(set(self.board[:,j]))==1:
                return "Won"
        # check for a win along diagonals
        if 2 not in np.diag(self.board) and len(set(np.diag(self.board)))==1:
            return "Won"
        if 2 not in np.diag(np.fliplr(self.board)) and len(set(np.diag(np.fliplr(self.board))))==1:
            return "Won"
        # check for a Draw
        if not 2 in self.board:
            return "Drawn"
        else:
            return "In Progress"

"""## Legal move Generator"""

def legal_moves_generator(current_board_state,turn_monitor):
    """Function that returns the set of all possible legal moves and resulting board states, 
    for a given input board state and player

    Args:
    current_board_state: The current board state
    turn_monitor: 1 if it's the player who places the mark 1's turn to play, 0 if its his opponent's turn

    Returns:
    legal_moves_dict: A dictionary of a list of possible next coordinate-resulting board state pairs
    The resulting board state is flattened to 1 d array

    """
    legal_moves_dict={}
    for i in range(current_board_state.shape[0]):
        for j in range(current_board_state.shape[1]):
            if current_board_state[i,j]==2:
                board_state_copy=current_board_state.copy()
                board_state_copy[i,j]=turn_monitor
                legal_moves_dict[(i,j)]=board_state_copy.flatten()
    return legal_moves_dict

"""## Evaluator"""

model = keras.models.load_model(model_path)

#model.summary()

"""## Program Move Selector"""

def move_selector(model,current_board_state,turn_monitor):
    """Function that selects the next move to make from a set of possible legal moves

    Args:
    model: The Evaluator function to use to evaluate each possible next board state
    turn_monitor: 1 if it's the player who places the mark 1's turn to play, 0 if its his opponent's turn

    Returns:
    selected_move: The numpy array coordinates where the player should place thier mark
    new_board_state: The flattened new board state resulting from performing above selected move
    score: The score that was assigned to the above selected_move by the Evaluator (model)

    """
    tracker={}
    legal_moves_dict=legal_moves_generator(current_board_state,turn_monitor)
    for legal_move_coord in legal_moves_dict:
        score=model.predict(legal_moves_dict[legal_move_coord].reshape(1,9))
        tracker[legal_move_coord]=score
    selected_move=max(tracker, key=tracker.get)
    new_board_state=legal_moves_dict[selected_move]
    score=tracker[selected_move]
    return selected_move,new_board_state,score

"""### 0 as an AI, 1 as a player"""

def playGame(model = model):
        # Location
    location = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1),
        9: (2, 2)
    }

    # Initialize game
    game = tic_tac_toe_game()

    # toss who play first
    game.toss()

    print("Starting the game!!!\n")
    print(f"Player {game.turn_monitor} play first\n")
    print(f"Initialize board: \n {game.board}")

    while(1):
        # Ai turn
        if game.game_status() == "In Progress" and game.turn_monitor == 0:
            # If its the program's turn, use the Move Selector function to select the next move
            selected_move,new_board_state,score = move_selector(model, game.board, game.turn_monitor)

            game_status, board = game.move(game.turn_monitor, selected_move)

            print("AI moved")
            print(board)
            print("\n")
        
        # Player turn
        elif game.game_status() == "In Progress" and game.turn_monitor == 1:
            try :
                player_move = int(input("Your turn to move: "))
                player_move = location[player_move]

            # Catch error
            except:
                player_move = int(input("Please make an valid move!: "))
                player_move = location[player_move]
            

            # player_move = tuple(player_move)
            print(player_move)

            game_status, board = game.move(game.turn_monitor, player_move)
            print("Player moved\n")
            print(board)
            print("\n")

        else:
            players = ["AI", "Player"]
        
            if game.game_status() == "Draw":
                print(f"{game.game_status}")
            else:
                print(f"{players[1 - game.turn_monitor]} has {game.game_status()} ")
            break

"""## The input should be the location that you want to play ranging from 1-9 : 

[[1, 2, 3]

[4, 5, 6]

[7, 8, 9]]
"""

# playGame()
