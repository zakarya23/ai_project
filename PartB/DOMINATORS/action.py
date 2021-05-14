from DOMINATORS.board import Board
from random import randrange
from numpy import inf
from random import shuffle
import math



def piece_dict(state):
    opp_piece_dic = {'r': 0, 'p': 0, 's': 0}
    our_piece_dic = {'r': 0, 'p': 0, 's': 0}
    
    # throw = None # name of the selected piece that we going to throw
    ours = state['board'].our
    opponent = state['board'].opponent
    for location in opponent:
        for p in opponent[location]:
            opp_piece_dic[p] += 1

    for location in ours:
        for p in ours[location]:
            our_piece_dic[p] += 1

    return opp_piece_dic, our_piece_dic

def first_action(state): 
    if state['throws'] == 0: 
        initial = randrange(0, 2)
        # print(f'a  ={initial}')
        if state['player_type'] == "upper":
            # print('a')
            state['throw_x'] = 4
            return (4, -initial)
        else:
            state['throw_x'] = -4
            # print('b')
            return (-4, initial)

def throw_what(state):
        throw = None
        opp_piece_dic, our_piece_dic = piece_dict(state)

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

def distance(p1, p2):    
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def danger(state): 
    distance = inf
    our = None
    opp = None
    for our_loc in state['board'].our:
        for opp_loc in state['board'].opponent: 
            # print(f'{our_loc} {opp_loc}')
            # dis = distance(our_loc, opp_loc)
            dis = 0
            if dis < distance and (len(state['board'].our[our_loc]) > 0) and (len(state['board'].opponent[opp_loc]) > 0): 
                distance = distance
                our = our_loc
                opp = opp_loc
    
    our_piece = state['board'].our[our][0]
    opp_piece = state['board'].opponent[opp][0]

    if state['pairs'][opp_piece] == our_piece:
        # A danger piece is close 
        return -1 
    elif state['pairs'][our_piece] == opp_piece:
        return 1 
    else: 
        return 0 

def closeness(state):

    if state['board'].our == [] or state['board'].opponent == []:
        return 9

    dist = []
    for p in state['board'].our:
        for o in state['board'].opponent:
            dist.append(distance(p, o))
    return min(dist)

def closest_opp(state):
    our_r, our_p, our_s = [] 
    opp_r, opp_p, opp_s =[] 
    opp_piece_dic, our_piece_dic = piece_dict(state)
    
    for p in our_piece_dic:
        if p.value() == 'r':
            our_r.append(p)
        if p.value() == 'p':
            our_p.append(p)
        else:
            our_s.append(p)
        for o in opp_piece_dic:
            if p.value() == 'r':
                opp_r.append(p)
            if p.value() == 'p':
                opp_p.append(p)
            else:
                opp_s.append(p)

    dist_r_s = closeness(our_r, opp_s)
    dist_p_r = closeness(our_p, opp_r)
    dist_s_p = closeness(our_s, opp_p)

    best_dist = 1/(min(dist_r_s, dist_p_r, dist_s_p))
    return best_dist

def eval(state): 
    #evaluation value components
        
    dist_size = 1
    token_size = 1 
    compete_size = 2 
    compete_val = 0
    dang_val = 0
    eval_val = 0
    invinciblity = 0
    token_val = 0
    
    # Utility: basically will check for a chance of winning like 
    # if the game ended: how to write this? 
    opp_piece_dic, our_piece_dic = piece_dict(state)

    compete_val += our_piece_dic['r'] - opp_piece_dic['p']
    compete_val += our_piece_dic['s'] - opp_piece_dic['r']
    compete_val += our_piece_dic['p'] - opp_piece_dic['s'] 
    # opponent_pieces = self.board.opponent
    
    # dist_val = closest_opp(state)
    
#     if number of our throws == 0 and number of opponent throws == 0:
#         invinciblity = 10

# # board state where opponent has no throws but player does have
#     elif opponent throw == 0:
#     # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
#         if invincible < 0:
#             invinciblity = 5
#     elif our number of throws == 0:
#     # If they currently have a more invinvible tokens but we can throw opposite type to negate so half the weight
#         if invincible > 0:
#             invinciblity = 5
    
    # eval_val += self.check_piece_future(location, opponent_pieces, piece)

    # Checking if we are close to the opposite opponent piece 
    dang_val += danger(state)

    # Idk why I put this here... 
    token_val += len(our_piece_dic.values())
    token_val -= len(opp_piece_dic.values())

    # eval_val = (token_val * token_size) + (dang_val) + (inviciblity * invicible) + (dist_size * dist_val) + (compete_size * compete_val)

    return eval_val

def minimax(current_piece, current_depth, piece, maximising, state, alpha: int=-inf, beta: int=inf):
        if current_depth == state['max_depth']:
            return eval(state)  
            # Evaluation function
        
        future_piece = None
        # get all possible actions and stored them in a list (NOT IMPLEMENTED YET)
        shuffle(state['board'].vectors) #random
        max_value = -inf if maximising else inf
        one = False
        for cell in state['board'].vectors:
            child = (current_piece[0] + cell[0], current_piece[1] + cell[1])
            if child in state['board'].spots: 
                eval_child = minimax(child, current_depth + 1, piece, not maximising, state, alpha, beta)
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

def best_move(state): 
    highest = -inf
    piece = None

    for locations in state['board'].our.keys():
        pieces = state['board'].our[locations]
        if len(pieces) > 0:
            for _ in pieces: 

                fp, new_score = minimax(locations, 0, pieces[0], True, state)

                if new_score > highest:
                    highest = new_score 
                    if fp: 
                        piece = fp
                      
            return locations, piece

def take_action(state):
    token = ["r", "s", "p"]
    sent = False
    board = Board()
    new = None

    # How to decide whether to throw or slide 
    if state['turn'] % 2 ==  0 and state["first_turn"]: 
        state["first_turn"] = False
        # First piece chosen randomly 
        r_index = randrange(len(token))
        
        sent = True
        throw_at = first_action(state)
        # print(throw_at)
        state["throws"] += 1
        # print(("THROW", token[r_index], (throw_at[0], throw_at[1])))
        return ("THROW", token[r_index], (throw_at[0], throw_at[1])) 

    elif state['turn'] % 2 ==  0 and state["throws"] < 9: 
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss")
        state['turn'] += 1
        state["throws"] += 1
        initial = randrange(0, 2)
        if (state['player_type'] == "upper"):
            new = (state['throw_x'], -initial)
            if new in board.spots: 
                sent = True
                # self.start = new
        else: 
            new = (state['throw_x'], initial)
            if new in board.spots:
                sent = True 
                # self.start = new
        piece = throw_what(state)
        if sent:
            print("POPOPOPO")
            return ("THROW", piece, (new[0], new[1])) 
    while not sent: 
        state['turn'] += 1
        piece = best_move(state)
        to_move = piece[0]
        move = piece[1]
        if to_move and move:
            return ("SLIDE", to_move, move)

    