from DOMINATORS.board import Board
from DOMINATORS.piece import Piece
from random import randrange
import numpy as np
import math
from random import shuffle
from matplotlib import pyplot as plt
from IPython.display import clear_output
import sys

# need to make sure not to kill our pieces
# improve throws 
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
        self.pairs = {'r':'s', 'p': 'r', 's':'p'}

    def piece_dict(self):
        opp_piece_dic = {'r': 0, 'p': 0, 's': 0}
        our_piece_dic = {'r': 0, 'p': 0, 's': 0}
        
        # throw = None # name of the selected piece that we going to throw
        ours = self.board.our
        opponent = self.board.opponent
        for location in opponent:
            for p in opponent[location]:
                opp_piece_dic[p] += 1

        for location in ours:
            for p in ours[location]:
                our_piece_dic[p] += 1

        return opp_piece_dic, our_piece_dic

    def throw_what(self):
        throw = None
        opp_piece_dic, our_piece_dic = self.piece_dict()

        # we need rock to kill the scissors
        if our_piece_dic['r'] == 0 and opp_piece_dic['s'] > 0:
            throw = 'r'
        # we need paper to kill the rocks
        if our_piece_dic['p'] == 0 and opp_piece_dic['r'] > 0:
            throw = 'p'
        # we need scissor to kill the paper
        if our_piece_dic['s'] == 0 and opp_piece_dic['p'] > 0:
            throw = 's'

        if throw:
            return throw
        else: 
            # Choose random piece
            token = ["r", "s", "p"]
            r_index = randrange(len(token))
            return token[r_index]
    
    def distance(self, p1, p2): 
        return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

    def danger(self): 
        distance = sys.maxsize
        our = None
        opp = None
        for our_loc in self.board.our:
            for opp_loc in self.board.opponent: 
                dis = self.distance(our_loc, opp_loc)
                if dis < distance and (len(self.board.our[our_loc]) > 0) and (len(self.board.opponent[opp_loc]) > 0): 
                    distance = distance
                    our = our_loc
                    opp = opp_loc
        
        our_piece = self.board.our[our][0]
        opp_piece = self.board.opponent[opp][0]

        if self.pairs[opp_piece] == our_piece:
            # A danger piece is close 
            return -1 
        elif self.pairs[our_piece] == opp_piece:
            return 1 
        else: 
            return 0 

    # def check_piece_future(self, location, opponent_pieces, piece): 
    #     if (location in opponent_pieces) and (len(opponent_pieces[location]) > 0): 
    #         opp = opponent_pieces[location][0]
    #         if self.pairs[opp] == piece:
    #             return -1 
    #         elif self.pairs[piece] == opp:
    #             return 1   
    #         else:
    #             return 0 
            
    def eval(self): 
        #evaluation value components
        
        dist_size = 1
        token_size = 1 
        compete_size = 2 
        
        # Utility: basically will check for a chance of winning like 
        # if the game ended: how to write this? 
        opp_piece_dic, our_piece_dic = self.piece_dict()

        compete_val += our_piece_dic['r'] - opp_piece_dic['p']
        compete_val += our_piece_dic['s'] - opp_piece_dic['r']
        compete_val += our_piece_dic['p'] - opp_piece_dic['s'] 
        opponent_pieces = self.board.opponent
        
        dist_val = closest_opp(self)
        
        if number of our throws == 0 and number of opponent throws == 0:
        invinciblity = 10

    # board state where opponent has no throws but player does have
        elif opponent throw == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
            if invincible < 0:
                invinciblity = 5
        elif our number of throws == 0:
        # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
            if invincible > 0:
                invinciblity = 5
        
        # eval_val += self.check_piece_future(location, opponent_pieces, piece)

        # Checking if we are close to the opposite opponent piece 
        dang_val += self.danger()

        # Idk why I put this here... 
        token_val += len(our_piece_dic.values())
        token_val -= len(opp_piece_dic.values())

        eval_val = (token_val * token_size) + (dang_val) + (inviciblity * invicible) + (dist_size * dist_val) + (compete_size * compete_val)
        
        return eval_val

    def minimax(self, current_piece, current_depth, piece, maximising, alpha: int=-sys.maxsize, beta: int=sys.maxsize):
        if current_depth == self.max_depth:
            return self.eval(current_piece, piece)  
            # Evaluation function
        
        future_piece = None
        # get all possible actions and stored them in a list (NOT IMPLEMENTED YET)
        shuffle(self.board.vectors) #random
        max_value = -sys.maxsize if maximising else sys.maxsize
        one = False
        for cell in self.board.vectors:
            child = (current_piece[0] + cell[0], current_piece[1] + cell[1])
            if child in self.board.spots: 
                eval_child = self.minimax(child, current_depth + 1, piece, not maximising, alpha, beta)
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

        return future_piece, max_value

    def best_move(self): 

        highest = -sys.maxsize
        piece = None

        for locations in self.board.our.keys():
            pieces = self.board.our[locations]
            if len(pieces) > 0:
                for _ in pieces: 

                    fp, new_score = self.minimax(locations, 0, pieces[0], True)

                    if new_score > highest:
                        highest = new_score 
                        if fp: 
                            piece = fp
                            # print(f'{piece} ={highest}')
                return locations, piece

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        token = ["r", "s", "p"]
        sent = False

        # How to decide whether to throw or slide 
        if self.turn % 2 ==  0 and self.first_turn: 
            self.first_turn = False
            # First piece chosen randomly 
            r_index = randrange(len(token))
            self.throws += 1
            sent = True
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif self.turn % 2 ==  0 and self.throws < 9: 
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
            piece = self.throw_what()
            if sent:
                return ("THROW", piece, (self.start[0], self.start[1])) 
        while not sent: 
            self.turn += 1
            piece = self.best_move()
            to_move = piece[0]
            move = piece[1]
            if to_move and move:
                return ("SLIDE", to_move, move)

    def battle_ourself(self, states, location, name):
        if len(states[location]) > 0:
            prev_pieces = states[location][0]
            new_piece = states[location][-1]
            if self.pairs[new_piece] == prev_pieces:
                # We remove all prev pieces and add new piece 
                states[location].clear()
                states[location].append(name)
            elif new_piece == prev_pieces: 
                states[location].append(name)
        else: 
            states[location].append(name)
    
    def battle_opponent(self, states, opponent, opponent_pieces, name, location): 
        if len(opponent_pieces) > 0: 
            opp_piece = opponent_pieces[0] 
            if self.pairs[name] == opp_piece:
                # New piece wins over opp and is added 
                opponent[location].clear()
                states[location] = [] 
                states[location].append(name)
            elif name == opp_piece:
                states[location] = [] 
                states[location].append(name)

    def update_throw(self, states, opponent, name, location): 
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


    def update_slide(self, states, opponent, old_location, new_location):
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
            if self.pairs[moved_piece] == prev_piece: 
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
                if self.pairs[moved_piece] == opp_piece:
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
     
    def closeness(self.board.our, self.board.opponent):

        if self.board.our == [] or self.board.opponent == []:
            return 9

        dist = []
        for p in self.board.our:
            for o in self.board.opponent:
                dist.append(distance(p, o))
        return min(dist)

    def closest_opp(self):
        our_r, our_p, our_s = [] 
        opp_r, opp_p, opp_s =[] 
        opp_piece_dic, our_piece_dic = self.piece_dict()
        
        for p in our_piece_dic:
            if r.value() == 'r':
                our_r.append(r)
            if p.value() == 'p':
                our_p.append(p)
            else:
                our_s.append(s)
         for o in opp_piece_dic:
            if r.value() == 'r':
                opp_r.append(r)
            if p.value() == 'p':
                opp_p.append(p)
            else:
                opp_s.append(s)

        dist_r_s = closeness(our_r, opp_s)
        dist_p_r = closeness(our_p, opp_r)
        dist_s_p = closeness(our_s, opp_p)

        best_dist = 1/(min(dist_r_s, dist_p_r, dist_s_p))
        return best_dist
    
