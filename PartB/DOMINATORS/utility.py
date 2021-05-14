import math
from numpy import inf

def piece_dict(state):
    '''
    Finds total number of each piece for 
    us and opponent
    '''
    opp_piece_dic = {'r': 0, 'p': 0, 's': 0}
    our_piece_dic = {'r': 0, 'p': 0, 's': 0}

    ours = state['board'].our
    opponent = state['board'].opponent
    for location in opponent:
        for p in opponent[location]:
            opp_piece_dic[p] += 1

    for location in ours:
        for p in ours[location]:
            our_piece_dic[p] += 1

    return opp_piece_dic, our_piece_dic
    
def defeat(p1, p2):
    type = ['r', 's', 'p']
    for t in range(3):
        w = type[t]
        l = type[(t+1)%3]
        if w == p1 and l == p2:
            return 1
        
        if w == p1 and l == p2:
            return -1
    return 0

def win_chance(state):
    '''
    A way to calculate what our chance is winning. 
    '''
    opp_piece_dic, our_piece_dic = piece_dict(state)
    our_pieces = list(our_piece_dic.values())
    opp_pieces = list(opp_piece_dic.values())

    chance = 0

    for p in our_pieces:
        winner = 0
        
        for o in opp_pieces:
            if defeat(p, o) == -1:
                winner = 1
            
            if defeat(p, o) == 1:
                winner = 1
        
        if winner != 1:
            chance += 1
    
    for o in our_pieces:
        winner = 0
        
        for o in opp_pieces:
            if defeat(o, p) == -1:
                winner = 1
            
            if defeat(p, o) == 1:
                winner = 1
        
        if winner != 1:
            chance -= 1

    #chance of invicibility 
    return chance 

def distance(p1, p2):    
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def danger(state): 
    '''
    Used in utility function to reduce the utility if we 
    are moving towards a opponent higher piece.
    '''
    distance = inf
    our = None
    opp = None
    for our_loc in state['board'].our:
        for opp_loc in state['board'].opponent: 
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

def closeness(our_piece, opp_piece, our_pieces, opponent_pieces):
    '''
    Finds the shortest distance in the points between enemies. 
    '''
    if len(our_pieces) == 0 or len(opponent_pieces) == 0:
        return 9

    dist = []
    for loc1 in our_pieces:
        for loc2 in opponent_pieces:
            p1_pieces = our_pieces[loc1]
            p2_pieces = opponent_pieces[loc2]
            if len(p1_pieces) > 0 and len(p2_pieces) > 0:
                if p1_pieces[0] == our_piece and p2_pieces[0] == opp_piece: 
                    dist.append(distance(p1_pieces[0], p2_pieces[0]))
    if len(dist) > 0:
        return min(dist)
    return 0

def closest_opp(state):
    '''
    Returns the closest opponent piece. 
    '''
    our_r, our_p, our_s = [], [], []
    opp_r, opp_p, opp_s = [], [], []
    opp_piece_dic, our_piece_dic = piece_dict(state)
    
    for p in our_piece_dic:
        if p == 'r':
            our_r.append(p)
        if p == 'p':
            our_p.append(p)
        else:
            our_s.append(p)
        for o in opp_piece_dic:
            if o == 'r':
                opp_r.append(o)
            if o == 'p':
                opp_p.append(o)
            else:
                opp_s.append(o)

    dist_r_s = closeness(our_r, opp_s, state['board'].our, state['board'].opponent)
    dist_p_r = closeness(our_p, opp_r, state['board'].our, state['board'].opponent)
    dist_s_p = closeness(our_s, opp_p, state['board'].our, state['board'].opponent)

    best_dist = 1/(min(dist_r_s, dist_p_r, dist_s_p) + 1)
    return best_dist

def eval(state): 
    '''
    Evaluation function for minimax function.
    '''
    #evaluation value components
    dist_size = 1
    token_size = 1.5
    compete_size = 2 
    throw_size = 1
    compete_val = 0
    token_val = 0
    invinciblity = 0
    throw_val = 0 
    
    # Utility: basically will check for a chance of winning like 
    # if the game ended: how to write this? 
    opp_piece_dic, our_piece_dic = piece_dict(state)

    compete_val += our_piece_dic['r'] - opp_piece_dic['p']
    compete_val += our_piece_dic['s'] - opp_piece_dic['r']
    compete_val += our_piece_dic['p'] - opp_piece_dic['s'] 
    # opponent_pieces = self.board.opponent
    
    dist_val = closest_opp(state)
    invincible = win_chance(state)
    throw_val = (9 - state['throws']) - (9 - state['opponent_throws'])
    if state['throws'] == 0 and state['opponent_throws']  == 0:
        invinciblity = 10

    # Board state where we still got throws but our opponent does not
    elif state['opponent_throws'] == 0:
      
        if invincible < 0:
            invinciblity = 5
    elif state['throws']  == 0 == 0:
      
        if invincible > 0:
            invinciblity = 5
    
    # Checking if we are close to the opposite opponent piece 
    dang_val = danger(state)
 
    token_val += len(our_piece_dic.values())
    token_val -= len(opp_piece_dic.values())
    eval_val = (token_val * token_size) + dang_val + (invinciblity * invincible) + (dist_size * dist_val) + (compete_size * compete_val) + (throw_val * throw_size)
    return int(eval_val)