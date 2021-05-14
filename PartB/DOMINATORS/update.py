def battle_ourself(states, location, name, state):
    '''
    If we battle ourself
    '''
    # Making sure we have some pieces there. 
    if len(states[location]) > 0:
        prev_pieces = states[location][0]
        new_piece = name
        if state['pairs'][new_piece] == prev_pieces:
            # The pieces already there lost. 
            # We remove all prev pieces and add new piece 
            states[location].clear()
            states[location].append(name)
        elif new_piece == prev_pieces: 
            # Else they the same and we append.
            states[location].append(name)
    else: 
        states[location].append(name)

def battle_opponent(states, opponent, opponent_pieces, name, location, state): 
    '''
    When we battle opponent
    '''
    if len(opponent_pieces) > 0: 
        opp_piece = opponent_pieces[0] 
        if state['pairs'][name] == opp_piece:
            # New piece wins over opp and is added 
            opponent[location].clear()
            states[location] = [] 
            states[location].append(name)
        elif name == opp_piece:
            states[location] = [] 
            states[location].append(name)

def update_throw(states, opponent, name, location, state): 
    '''
    Updates throw for both us and opponent 
    '''
    if location not in states: 
        if location in opponent and len(opponent[location]) > 0: 
            opponent_pieces = opponent[location]
            battle_opponent(states, opponent, opponent_pieces[0] , name, location, state)
        else: 
            states[location] = [] 
            states[location].append(name)
    else:
        # Thrown on ours
        battle_ourself(states, location, name, state)

def update_slide(states, opponent, old_location, new_location, state):
    '''
    Updates slide for both us and opponent
    '''
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
        if state['pairs'][moved_piece] == prev_piece: 
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
            if state['pairs'][moved_piece] == opp_piece:
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

def update_states(player_action, opponent_action, state):
    '''
    Main function called in main to update state of the game. 
    '''
    # Update ours first 
    if player_action[0] == 'THROW':
        name = player_action[1] 
        location = player_action[2]     
        update_throw(state['board'].our, state['board'].opponent, name, location, state)
        state['throws'] += 1
    else: 
        old_location = player_action[1] 
        new_location = player_action[2] 
        update_slide(state['board'].our, state['board'].opponent, old_location, new_location, state)

    # Update opponents
    if opponent_action[0] == 'THROW':
        name = opponent_action[1] 
        location = opponent_action[2]
        update_throw(state['board'].opponent, state['board'].our, name, location, state)
        state['opponent_throws'] += 1
    else: 
        old_location = opponent_action[1] 
        new_location = opponent_action[2] 
        update_slide(state['board'].opponent, state['board'].our, old_location, new_location, state)