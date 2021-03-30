from search.piece import Piece

def sort_pieces(pieces):
    for key in pieces: 
        new_value = sorted(pieces[key])
        pieces[key] = new_value

def format_input(data): 
    blocked_set = make_blocked(data['block'])
    upper_pieces = make_dict(data['upper'])
    lower_pieces = make_dict(data['lower'])
    to_kill = all_goals(data['lower'])
    return upper_pieces, lower_pieces, blocked_set, to_kill

def all_goals(goals): 
    '''
    Stores all the pieces we need to kill 
    '''
    targets = [] 
    for goal in goals: 
        targets.append((goal[1], goal[2]))
    return targets

def make_dict(values): 
    final_dict = {} 
    for value in values: 
        piece = value[0]
        r = value[1]
        q = value[2]
        if piece in final_dict: 
            final_dict[piece].append((r, q))
        else: 
            final_dict[piece] = [] 
            final_dict[piece].append((r, q))
    return final_dict

def make_blocked(values): 
    blocked_set = set() 
    for block in values: 
            piece = (block[1], block[2])
            blocked_set.add(piece)
    return blocked_set