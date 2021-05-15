from random import randrange
from numpy import inf
from random import shuffle
from DOMINATORS.utility import eval
from DOMINATORS.helpers import scoring

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

def neighbours(location, state):
    all_neigh = [] 
    for point in state['board'].vectors: 
        new_point = (location[0] + point[0], location[1] +  point[1])
        if new_point in state['board'].spots:
            all_neigh.append(new_point)
    return all_neigh

def first_action(state): 
    '''
    Outputs a random location and random piece to 
    be thrown at the first throw.
    '''
    # Choosing a random piece
    token = ["r", "s", "p"]
    r_index = randrange(len(token))
    piece = token[r_index]
    # Making sure its first turn 
    if state['throws'] == 0: 
        initial = randrange(0, 2)
        if state['player_type'] == "upper":
            state['throw_x'] = 4
            point = (4, -initial)
            return ("THROW", piece, point) 
        else:
            state['throw_x'] = -4
            point = (-4, initial)
            return ("THROW", piece, point) 

def throw_what(state):
        '''
        Decides what to throw based on the current state of 
        our pieces in the game.
        '''
        throw = None
        opp_piece_dic, our_piece_dic = piece_dict(state)

        # We need rock to kill the scissors
        if our_piece_dic['r'] == 0 and opp_piece_dic['s'] > 0:
            throw = 'r'
        # We need paper to kill the rocks
        if our_piece_dic['p'] == 0 and opp_piece_dic['r'] > 0:
            throw = 'p'
        # We need scissor to kill the paper
        if our_piece_dic['s'] == 0 and opp_piece_dic['p'] > 0:
            throw = 's'

        if throw:
            return throw
        else: 
            # Else we choose random piece
            token = ["r", "s", "p"]
            r_index = randrange(len(token))
            return token[r_index]

def minimax(current_piece, current_depth, piece, maximising, state, alpha: int=-inf, beta: int=inf):
        if current_depth == state['max_depth']:
            # Evaluation function
            return eval(state)  
        # Will store the place we will move the piece. 
        future_piece = None
        shuffle(state['board'].vectors) # Random
        max_value = -inf if maximising else inf
        # Sometimes our function returns one value and sometimes a tuple of values. 
        # This boolean is to check what was returned so we handle it accordingly. 
        one = False
        # Go through all possible neighbours.
        # for cell in state['board'].vectors:
        for child in neighbours(current_piece, state):
            # Run minimax on it. 
            # if child not in state['board'].our: 
            eval_child = minimax(child, current_depth + 1, piece, not maximising, state, alpha, beta)
            # Here we check what type was returned. 
            if (type(eval_child) == int): 
                one = True
            # Find max accordingly. 
            if one and maximising and max_value < eval_child:
                max_value = eval_child
                future_piece =  child
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            # For tuple returned. 
            elif not one and maximising and max_value < eval_child[1]:
                max_value = eval_child[1]
                future_piece =  child
                alpha = max(alpha, max_value)
                one = False
                if beta <= alpha:
                    break
            # Find min accordingly.
            elif one and (not maximising) and max_value > eval_child:
                max_value = eval_child
                future_piece =  child
                beta = min(beta, max_value)
                if beta <= alpha:
                    break
            # For tuple returned. 
            elif not one and (not maximising) and max_value > eval_child[1]:
                max_value = eval_child[1]
                future_piece =  child
                beta = min(beta, max_value)
                one = False
                if beta <= alpha:
                    break
        return future_piece, max_value

def best_move(state): 
    '''
    Calculates and returns the best move based on 
    the minimax algorithm.
    '''
    # Set highest value to negative infinity. 
    highest = -inf
    # Will store the piece location we will be returning. 
    piece = None
    # From which location we will move from. 
    move_from = None
    # Iterate over locations where we have pieces.
    for locations in state['board'].our.keys():
        # Get what pieces we have at that location.
        pieces = state['board'].our[locations]
        # Make sure we do have something there and an 
        # empty list was not returned. 
        if len(pieces) > 0:
            # Run minimax on the location and its piece. 
            fp, new_score = minimax(locations, 0, pieces[0], True, state)
            # If highest then we change. 
            if new_score > highest:
                highest = new_score 
                # If piece exists then we can move it. 
                if fp: 
                    move_from = locations
                    piece = fp          
    return move_from, piece

def throw(piece, at): 
    return ("THROW", piece, at)

def slide(prev, to):
    return ("SLIDE", prev, to)

def swing(prev, to): 
    return ("SWING", prev, to)

def check_swings(l1, l2, state):
    swings = neighbours(l2, state)
    final_swings = [] 
    for s in swings: 
        if s not in state['board'].our: 

            # final_swings.append(swing(l1, l2))
            return final_swings

def check_slides(loc, state):
    final_slides = []
    piece = best_move(state)
    if piece:
        to_move = piece[0]
        move = piece[1]
        if to_move and move:
            final_slides.append(slide(to_move, move))
    return final_slides

def possible_moves(state):
    throws, slides, swings = [], [], [] 

    # Throws 
    if state['throws'] < 9: 
        state['turn'] += 1
        initial = randrange(0, 2)
        if (state['player_type'] == "upper"):
            new = (state['throw_x'], -initial)
            if new in state['board'].spots: 
                sent = True
        else: 
            new = (state['throw_x'], initial)
            if new in state['board'].spots:
                sent = True 
        piece = throw_what(state)
        if sent:
            throws += [("THROW", piece, new)]
        

    # Slides 
    for location in state['board'].our: 
        slides += (check_slides(location, state))

    # Swings
    # for location1 in state['board'].our: 
    #     for location2 in state['board'].our: 
    #         if location1 != location2 and (location2 in neighbours(location1, state)): 
    #             swings += (check_swings(location1, location2, state))

    total = throws + slides
    return total

def take_action(state):
    '''
    Called in main to return the main action 
    that is to be taken. 
    '''
    # An action was found
    sent = False
    # The piece to be thrown
    new = None

    # First turn 
    if state['turn'] % 2 ==  0 and state["first_turn"]: 
        state["first_turn"] = False
        sent = True
        return first_action(state)
    elif state['turn'] % 2 ==  0 and state["throws"] < 9: 
        state['turn'] += 1
        initial = randrange(0, 2)
        if (state['player_type'] == "upper"):
            new = (state['throw_x'], -initial)
            if new in state['board'].spots: 
                sent = True
        else: 
            new = (state['throw_x'], initial)
            if new in state['board'].spots:
                sent = True 
        piece = throw_what(state)
        if sent:
            return ("THROW", piece, new) 
    while not sent: 
        state['turn'] += 1
        piece = best_move(state)
        if piece:
            to_move = piece[0]
            move = piece[1]
            if to_move and move:
                return ("SLIDE", to_move, move)
