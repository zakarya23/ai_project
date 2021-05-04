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

    def check_piece(self, position):
        # print("aaaa")
        for opp in self.board.opponents: 
            if position.current == opp.current: 
                # print('battled')
                if position.name == "r" and opp.name == "s" or position.name == "p" and opp.name == "r" or position.name == "s" and opp.name == "p":
                    # print("haha")
                    return 1
                    # ind = self.board.opponents.index(p2)
                    # self.board.opponents.pop(ind)
                elif opp.name == "r" and position.name == "s" or opp.name == "p" and position.name == "r" or opp.name == "s" and position.name == "p":
                    # print("p2")
                    return -1
                    # ind = self.board.our_pieces.index(p1)
                    # self.board.our_pieces.pop(ind) 

            for opp in self.board.our_pieces: 
                # print(opp.name)
                if position.current == opp.current: 
                    # print('battled')
                    if position.name == "r" and opp.name == "s" or position.name == "p" and opp.name == "r" or position.name == "s" and opp.name == "p":
                        # print("haha")
                        return 1
                        # ind = self.board.opponents.index(p2)
                        # self.board.opponents.pop(ind)
                    elif opp.name == "r" and position.name == "s" or opp.name == "p" and position.name == "r" or opp.name == "s" and position.name == "p":
                        # print("p2")
                        return -1
        return 0 
        
    
    
    
    # def winning_position(self): maybe best_move is enough, what do you think? 

    
    # this function check if the winning chance is 100% and stop the minimax
    def absolute_win(self):
        opp_piece_dic, our_piece_dic = self.piece_dict()
        
        # when we both don't have anymore throws
        if opp_piece_dic['r'] == opp_piece_dic['p'] == 0 and opp_piece_dic['s'] != 0:
            if our_piece_dic['s'] == our_piece_dic['p'] == 0 and our_piece_dic['r'] != 0:
                win = True

        if opp_piece_dic['r'] == opp_piece_dic['s'] == 0 and opp_piece_dic['p'] != 0:
            if our_piece_dic['r'] == our_piece_dic['p'] == 0 and our_piece_dic['s'] != 0:
                win = True
        
        if opp_piece_dic['p'] == opp_piece_dic['s'] == 0 and opp_piece_dic['r'] != 0:
            if our_piece_dic['r'] == our_piece_dic['s'] == 0 and our_piece_dic['p'] != 0:
                win = True

        
        return win
    


    
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
            child = (current_piece.current[0] + cell[0], current_piece.current[1] + cell[1])
            if child in self.board.spots: 
                child_piece = Piece(child, current_piece.name)
                
                eval_child = self.minimax(child_piece, current_depth + 1, not maximising, alpha, beta)
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

    # evaluate the pair of actions using payoff matrix
    def eval(self): 
        eval_val = 0
        utility = 0

        # Utility: basically will check for a chance of winning like 
        # if the game ended: how to write this? 
        opp_piece_dic, our_piece_dic = self.piece_dict()
        
        for p in self.board.opponents:
            # if it got killed
            if (not p.status):
                utility += 1
        
        for p in self.board.opponents:
            # if it got killed
            if (not p.status):
                utility -= 1

        eval_val += our_piece_dic['r'] - opp_piece_dic['p']
        eval_val+= our_piece_dic['s'] - opp_piece_dic['r']
        eval_val += our_piece_dic['p'] - opp_piece_dic['s'] 
        
        # Evaluating and making it heuristic
        # print(f'here is {eval_val}')
        return eval_val
        

    # this function will check the rate of danger for getting distroyed by the opponent piece like how close is the dominant piece to it
    def danger_check(self, piece):

        if piece: 
            return None



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
        
        for p in self.board.our_pieces: 
            # print(f'{p.current} {p.status}')
            # def minimax(self, current_piece, current_depth, maximising, alpha: int= - sys.maxsize, beta: int=sys.maxsize):
            if p.status:
                # print("used")
                fp, new_score = self.minimax(p, 0, True)
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
        
    def throw(self, sent): 
        token = ["r", "s", "p"]
        self.turn += 1
        self.throws += 1
        if (self.move == "ADD"):
            new = (self.start[0] + 1, self.start[1])
            if new in self.board.spots and new not in self.board.our_locations: 
                sent = True
                self.start = new
        else: 
            new =  self.start = (self.start[0] - 1, self.start[1])
            if new in self.board.spots and new not in self.board.our_locations:
                sent = True 
                self.start = new

        r_index = randrange(len(token))
        # print("AAAAA")    
        if sent:
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 

    
    # this will choose what piece to throw between (r, s, p) use it inside action func while we have throws option
    # we don't need to throw all of our pieces in order to win, remember less pieces = faster game
    def piece_dict(self):
        opp_piece_dic = {'r': 0, 'p': 0, 's': 0}
        our_piece_dic = {'r': 0, 'p': 0, 's': 0}
        
        throw = None #name of the selected piece that we going to throw
        for p in self.board.opponents:
            for key in opp_piece_dic:
                if p == key:
                    opp_piece_dic[key] += 1
        
        for p in self.board.our_pieces:
            for key in our_piece_dic:
                if p == key:
                    our_piece_dic[key] += 1
        return opp_piece_dic, our_piece_dic
    
    
    def throw_what(self):
        
        opp_piece_dic, our_piece_dic = self.piece_dict()
        # these will make us win faster and increase the chance of winning instead of random throwing
        
        # we need rock to kill the scissors
        if our_piece_dic['r'] == 0 and opp_piece_dic['s'] > 0:
            throw = 'r'
        # we need paper to kill the rocks
        if our_piece_dic['p'] == 0 and opp_piece_dic['r'] > 0:
            throw = 'p'
      
        # we need scissor to kill the paper
        if our_piece_dic['s'] == 0 and opp_piece_dic['p'] > 0:
            throw = 's'
        

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
                if new in self.board.spots and new not in self.board.our_locations: 
                    sent = True
                    self.start = new
            else: 
                new =  self.start = (self.start[0] - 1, self.start[1])
                if new in self.board.spots and new not in self.board.our_locations:
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


            return ("SLIDE", to_move.current, move)

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        o = None
        p = None

        if opponent_action[0] == "THROW": 
            opp_piece = Piece(opponent_action[2], opponent_action[1]) 
            self.board.opponents.append(opp_piece)  
            o = opp_piece
        else: 
            old_location = opponent_action[1]
            # Searching for which piece had that initial location
            for piece in self.board.opponents: 
                # If location matches we update its position
                if piece.current == old_location and piece.status: 
                    piece.current = opponent_action[2] 
                    o = piece
                    break 

        if player_action[0] == 'THROW': 
            p_piece =  Piece(player_action[2], player_action[1])  
            self.board.our_pieces.append(p_piece)
            self.board.our_locations.append(player_action[2])
            p = p_piece
        else: 
            old_location = player_action[1]

            # Searching for which piece had that initial location
            for piece in self.board.our_pieces: 

                # If location matches we update its position
                if piece.current == old_location and piece.status: 
                    i = self.board.our_locations.index(piece.current)
                    self.board.our_locations.pop(i)
                    piece.current = player_action[2]
                    self.board.our_locations.append(piece.current)
                    p = piece
                    break

        def verse(self, p1, p2): 
            if p1.name == "r" and p2.name == "s" or p1.name == "p" and p2.name == "r" or p1.name == "s" and p2.name == "p":
                ind = self.board.opponents.index(p2)
                self.board.opponents.pop(ind)   
            elif p2.name == "r" and p1.name == "s" or p2.name == "p" and p1.name == "r" or p2.name == "s" and p1.name == "p":
                ind = self.board.our_pieces.index(p1)
                self.board.our_pieces.pop(ind) 

        # Checking if something was thrown onto my pieces 
        for piec in self.board.our_pieces: 
            if piec.current == opponent_action[2] and (o in self.board.opponents) and o.status:
                if piec.name == "r" and o.name == "s" or piec.name == "p" and o.name == "r" or piec.name == "s" and o.name == "p":
                    o.status = False
                elif o.name == "r" and piec.name == "s" or o.name == "p" and piec.name == "r" or o.name == "s" and piec.name == "p":
                    piec.status = False

        # Check if we hurt enemey 
        for oppo in self.board.opponents: 
            if oppo.current == player_action[2] and (p in self.board.our_pieces) and p.status: 
                if p.name == "r" and oppo.name == "s" or p.name == "p" and oppo.name == "r" or p.name == "s" and oppo.name == "p":
                    oppo.status = False
                elif oppo.name == "r" and p.name == "s" or oppo.name == "p" and p.name == "r" or oppo.name == "s" and p.name == "p":
                    p.status = False
 
        # We killed ourself 
        for pie in self.board.our_pieces: 
            if pie.current == player_action[2]:
                if pie.name == "r" and p.name == "s" or pie.name == "p" and p.name == "r" or pie.name == "s" and p.name == "p":
                    p.status = False
                elif p.name == "r" and pie.name == "s" or p.name == "p" and pie.name == "r" or p.name == "s" and pie.name == "p":
                    pie.status = False

        # opp killed itself
        for opp in self.board.opponents: 
            if opp.current == opponent_action[2] and o in self.board.opponents:
                if opp.name == "r" and o.name == "s" or opp.name == "p" and o.name == "r" or opp.name == "s" and o.name == "p":
                    o.status = False
                elif o.name == "r" and opp.name == "s" or o.name == "p" and opp.name == "r" or o.name == "s" and opp.name == "p":
                    opp.status = False