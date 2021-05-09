from DOMINATORS.board import Board
from DOMINATORS.piece import Piece
from random import randrange
from DOMINATORS.node import Node
import numpy as np
import math
import random
from random import shuffle
from matplotlib import pyplot as plt
from IPython.display import clear_output
import sys


class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.
        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here 
        # If upper is given to us we can start with x = 4 and y is anything in the given range
        if player == "upper": 
            self.start = (4, 0)
            self.move = "SUBTRACT"
        else: 
            self.start = (-4, 0)
            self.move = "ADD"
        
        self.player_type = player
        self.board = Board()
        self.turn = 0 
        self.first_turn = True 
        self.throws = 0 
        self.max_depth = 3

    def eval(self): 
        eval_val = 0
        utility = 0

        # Utility: basically will check for a chance of winning like 
        # if the game ended: how to write this? 
        # opp_piece_dic, our_piece_dic = self.piece_dict()
        
        # for p in self.board.opponents:
        #     # if it got killed
        #     if (not p.status):
        #         utility += 1
        
        # for p in self.board.opponents:
        #     # if it got killed
        #     if (not p.status):
        #         utility -= 1

        # eval_val += our_piece_dic['r'] - opp_piece_dic['p']
        # eval_val+= our_piece_dic['s'] - opp_piece_dic['r']
        # eval_val += our_piece_dic['p'] - opp_piece_dic['s'] 
        
        # Evaluating and making it heuristic
        # print(f'here is {eval_val}')
        return eval_val

    def minimax(self, current_piece, current_depth, maximising, alpha: int= - sys.maxsize, beta: int=sys.maxsize):
        if current_depth == self.max_depth:
            return self.eval()  
            # Evaluation function
        
        future_piece = None
        # get all possible actions and stored them in a list (NOT IMPLEMENTED YET)
        shuffle(self.board.vectors) #random
        max_value = -sys.maxsize if maximising else sys.maxsize
        one = False
        for cell in self.board.vectors:
            child = (current_piece[0] + cell[0], current_piece[1] + cell[1])
            if child in self.board.spots: 
                eval_child = self.minimax(child, current_depth + 1, not maximising, alpha, beta)
                if (type(eval_child) == int): 
                    one = True

                if one and maximising and max_value < eval_child:
                    max_value = eval_child
                    future_piece =  child
                    alpha = max(alpha, max_value)
                    if beta <= alpha:
                        break
                elif not one and maximising and max_value < eval_child[1]:
                    max_value = eval_child[1]
                    future_piece =  child
                    alpha = max(alpha, max_value)
                    one = False
                    if beta <= alpha:
                        break
                
                elif one and (not maximising) and max_value > eval_child:
                    max_value = eval_child
                    future_piece =  child
                    beta = min(beta, max_value)
                    if beta <= alpha:
                        break

                elif not one and (not maximising) and max_value > eval_child[1]:
                    max_value = eval_child[1]
                    future_piece =  child
                    beta = min(beta, max_value)
                    one = False
                    if beta <= alpha:
                        break

        return future_piece , max_value

    def best_move(self): 

        highest = -sys.maxsize
        piece = None

        for locations in self.board.our.keys():
            pieces = self.board.our[locations]
            if len(pieces) > 0:
                for _ in pieces: 

                    fp, new_score = self.minimax(locations, 0, True)
                    if new_score > highest:
                        highest = new_score 
                        if fp: 
                            piece = fp
                return locations, fp

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        token = ["r", "s", "p"]
        sent = False

        # put your code here
        # How to decide whether to throw or slide 
        if self.turn % 2 ==  0 and self.first_turn: 
            self.first_turn = False
            # self.turn += 1
            r_index = randrange(len(token))
            self.throws += 1
            sent = True
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif self.turn % 2 ==  0 and self.throws < 9: 
            # How to calculate new throw position
            token = ["r", "s", "p"]
            self.turn += 1
            self.throws += 1
            if (self.move == "ADD"):
                new = (self.start[0] + 1, self.start[1])
                if new in self.board.spots: 
                    sent = True
                    self.start = new
            else: 
                new = (self.start[0] - 1, self.start[1])
                if new in self.board.spots:
                    sent = True 
                    self.start = new

            r_index = randrange(len(token))
            if sent:
                return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        while not sent: 
            self.turn += 1
            piece = self.best_move()
            to_move = piece[0]
            move = piece[1]


            return ("SLIDE", to_move, move)

    def battle_ourself(self, states, location, name):
        pairs = {'r':'s', 'p': 'r', 's':'p'}
        prev_pieces = states[location][0]
        new_piece = states[location][-1]
        if pairs[new_piece] == prev_pieces:
            # We remove all prev pieces and add new piece 
            states[location].clear()
            states[location].append(name)
        elif new_piece == prev_pieces: 
            states[location].append(name)
    
    def battle_opponent(self, states, opponent, opponent_pieces, name, location): 
        pairs = {'r':'s', 'p': 'r', 's':'p'}
        if len(opponent_pieces) > 0: 
            opp_piece = opponent_pieces[0] 
            if pairs[name] == opp_piece:
                # New piece wins over opp and is added 
                opponent[location].clear()
                states[location] = [] 
                states[location].append(name)
            elif name == opp_piece:
                states[location] = [] 
                states[location].append(name)

    def update_throw(self, states, opponent, name, location): 
        # pairs = {'r':'s', 'p': 'r', 's':'p'}
        if location not in states: 
            if location in opponent and len(opponent[location]) > 0: 
                opponent_pieces = opponent[location]
                self.battle_opponent(states, opponent, opponent_pieces[0] , name, location)
            else: 
                states[location] = [] 
                states[location].append(name)

        else:
            # Thrown on ours
            self.battle_ourself(states, location, name)
            # Thrown on opponent
            # self.battle_at_throw(opponent, location, name)

        # print(f'states {states}')

    def update_slide(self, states, opponent, old_location, new_location):
        pairs = {'r':'s', 'p': 'r', 's':'p'}
        # Can only be one type of piece 

        if old_location not in states:
            return None
        old_pieces = states[old_location]

        if len(old_pieces) == 0: 
            states.pop(old_location)
            return None
        else:
            moved_piece = old_pieces.pop(0)

        # Check if we slid onto our pieces 
        # Means something was there before
        if (new_location in states) and len(states[new_location]) > 0: 
            prev_pieces = states[new_location]
            prev_piece = prev_pieces[0] 
            if pairs[moved_piece] == prev_piece: 
                # New piece won and killed all our others 
                states[new_location].clear() 
                # Killed opponents too
                if new_location in opponent:
                    opponent[new_location].clear() 
                states[new_location].append(moved_piece)
            elif moved_piece == prev_piece: 
                states[new_location].append(moved_piece)
        # Else we dont have it in. So we check if opponent has it.
        else:
            if (new_location in opponent) and (len(opponent[new_location]) > 0):
                opp_pieces = opponent[new_location]
                opp_piece = opp_pieces[0] 
                if pairs[moved_piece] == opp_piece:
                    # New piece won and killed all our others 
                    opponent[new_location].clear() 
                    states[new_location] = [] 
                    states[new_location].append(moved_piece)
                elif moved_piece == opp_piece:
                    states[new_location] = [] 
                    states[new_location].append(moved_piece)
            else: 
                states[new_location] = [] 
                states[new_location].append(moved_piece)

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        
        # Update ours first 
        if player_action[0] == 'THROW':
            name = player_action[1] 
            location = player_action[2]
            self.update_throw(self.board.our, self.board.opponent, name, location)
        else: 
            old_location = player_action[1] 
            new_location = player_action[2] 
            self.update_slide(self.board.our, self.board.opponent, old_location, new_location)
   
        # Update opponents
        if opponent_action[0] == 'THROW':
            name = opponent_action[1] 
            location = opponent_action[2]
            self.update_throw(self.board.opponent, self.board.our, name, location)
        else: 
            old_location = opponent_action[1] 
            new_location = opponent_action[2] 
            self.update_slide(self.board.opponent, self.board.our, old_location, new_location)