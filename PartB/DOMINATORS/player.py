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
               
        # how to check the game if its ended? right it here
        
        # then we need to repeat minimax for another piece

       
        if current_depth == self.max_depth: # or self.ended()
                                         #?? how to ceck end of game

            # print("e")
            return self.eval()  
            # Evaluation function
        
        future_piece = None
        # get all possible actions and stored them in a list (NOT IMPLEMENTED YET)
        # print("else")
        shuffle(self.board.vectors) #random
        max_value = -sys.maxsize if maximising else sys.maxsize
        one = False
        for cell in self.board.vectors:
            # print(current_piece.current[0])
            child = (current_piece[0] + cell[0], current_piece[1] + cell[1])
            if child in self.board.spots: 
                # child_piece = Piece(child, current_piece.name)
                
                eval_child = self.minimax(child, current_depth + 1, not maximising, alpha, beta)
                # print("A")

                
                if (type(eval_child) == int): 
                    # print("is int")
                    # print(f'eval = {eval_child}')
                    one = True
                # else: 
                #     print("not int")
                #     print(f'eval = {eval_child}')
                    
                
                
                # print(max_value)
                if one and maximising and max_value < eval_child:
                    # print("AA")
                    max_value = eval_child
                    future_piece =  child
                    alpha = max(alpha, max_value)
                    one = False
                    if beta <= alpha:
                        # print("b1")
                        break
                elif not one and maximising and max_value < eval_child[1]:
                    # print("AA")
                    max_value = eval_child[1]
                    future_piece =  child
                    alpha = max(alpha, max_value)
                    one = False
                    if beta <= alpha:
                        # print("b1")
                        break
                
                elif one and (not maximising) and max_value > eval_child:
                    # print("Bb")
                    max_value = eval_child
                    future_piece =  child
                    beta = min(beta, max_value)
                    one = False
                    if beta <= alpha:
                        # print("b2")
                        break
                elif not one and (not maximising) and max_value > eval_child[1]:
                    # print("Bb")
                    max_value = eval_child[1]
                    future_piece =  child
                    beta = min(beta, max_value)
                    one = False
                    if beta <= alpha:
                        # print("b2")
                        break
            


        return future_piece , max_value

    def best_move(self): 
        #heuristic dict
        
        # store all the empty cells

        # highest = -sys.maxsize
        # piece = None
        # # a = True
        # count = 0 
        # for p in self.board.our_pieces: 
        #     print(f'ours {p.current} {p.status}')

        # for p in self.board.opponents: 
        #     print(f'opps {p.current} {p.status}')
        for locations in self.board.our.keys():
            pieces = self.board.our[locations]
        
            for p in pieces: 
                # print(f'{p.current} {p.status}')
                # def minimax(self, current_piece, current_depth, maximising, alpha: int= - sys.maxsize, beta: int=sys.maxsize):
            
                    # print("used")
                fp, new_score = self.minimax(locations, 0, True)
                if fp: 
                    # print(f'p, fp = {p}, {fp}')
                    return p, fp
                    
           
            
        #    print("P")
        #    if new_score > highest: 
        #        print("high")
        #        highest = new_score
        #        piece = fp
        #        break
        # if piece:
        #     return piece

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
            # self.turn += 1
            self.throws += 1
            if (self.move == "ADD"):
                new = (self.start[0] + 1, self.start[1])
                if new in self.board.spots: 
                    sent = True
                    self.start = new
            else: 
                new =  self.start = (self.start[0] - 1, self.start[1])
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

    def update_throw(self, states, name, location): 
        if location not in states: 
            states[location] = [] 
            states[location].append(name)
        else: 
            states[location].append(name)

    def update_slide(self, states, old_location, new_location):
        pieces = states[old_location]
        # Big assumption that we choose first element we choose
        first_piece = pieces[0] 
        states[old_location].pop(0)
        if new_location not in states:
            states[new_location] = [] 
            states[new_location].append(first_piece)
        else: 
            states[new_location].append(first_piece)

        

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        pairs = {'r':'s', 'p': 'r', 's':'p'}
        
        # Update ours first 
        if player_action[0] == 'THROW':
            name = player_action[1] 
            location = player_action[2]
            self.update_throw(self.board.our, name, location)
        else: 
            old_location = player_action[1] 
            new_location = player_action[2] 
            self.update_slide(self.board.our, old_location, new_location)
   
        # Update opponents
        if opponent_action[0] == 'THROW':
            name = opponent_action[1] 
            location = opponent_action[2]
            self.update_throw(self.board.opponent, name, location)
        else: 
            old_location = opponent_action[1] 
            new_location = opponent_action[2] 
            self.update_slide(self.board.opponent, old_location, new_location)

        # Check battles against opponent
        for p1_location in self.board.our: 
            for p2_location in self.board.opponent: 
                if p1_location == p2_location: 
                    p1_pieces = self.board.our[p1_location]
                    p2_pieces = self.board.opponent[p2_location]

                    p1_killed = [] 
                    p2_killed = [] 
                    for p1 in p1_pieces: 
                        for p2 in p2_pieces: 
                            if pairs[p1] == p2: 
                                # P1 killed p2 
                                p2_killed.append(p2_pieces.index(p2))
                            elif pairs[p2] == p1: 
                                # P2 KILLED P1 
                                p1_killed.append(p1_pieces.index(p1))
                        for i in p2_killed: 
                            self.board.opponent[p2_location].pop(i)

                    for j in p1_killed: 
                            self.board.our[p1_location].pop(j)

                        
                            



            

            



         

        

     