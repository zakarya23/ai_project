"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import math
from queue import PriorityQueue

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing
import search.node as Node
from search.piece import Piece

def make_solution(inital, goal, blocked): 
    unvisited = PriorityQueue()
    visited = [] 
    target = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
    # Format is [distance to goal, (x, y)]
    start = [0, (inital[0], inital[1])]
    unvisited.put(start)
    not_found = True

    while not unvisited.empty() and not_found: 
        current = unvisited.get(0)
        for next_position in target: 
            new_point = (current[1][0] + next_position[0], current[1][1] + next_position[1])
            if new_point in blocked: 
                continue
            if (new_point == goal): 
                not_found = False
                break
            distance_to_goal = math.sqrt(abs(goal[0] - new_point[0]) + abs(goal[1] - new_point[1]))
            unvisited.put([distance_to_goal, (new_point)])
        visited.append(current)

    # Will give final path to follow
    visited.append([0, goal])
    # Normalising so that we dont need to use distance anymore for further calculations
    normalised = [] 
    for route in visited:
        normalised.append(route[1])
    return normalised

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

def sort_pieces(pieces):
    for key in pieces: 
        new_value = sorted(pieces[key])
        pieces[key] = new_value

def get_routes(upper, lower, pieces, blocked_set, initial, target): 
    if initial not in upper or target not in lower: 
        return None
    initials = upper[initial]
    for piece in initials: 
        all_targets = lower[target]
        # print(all_targets)
        goal = None
        if len(all_targets) > 0:
            goal = all_targets.pop()
            initials.pop()
        if goal: 
            route = make_solution(piece, goal, blocked_set)
            piece = Piece(piece, route, initial, 0)
            pieces.append(piece)

# piece = inital 
# goal is target
def get_new_route(pieces, initial, lower, name, target, blocked_set): 
    all_targets = lower[target]
    goal = None
    if (len(all_targets) > 0): 
        goal = all_targets.pop()
    if goal: 
        route = make_solution(initial, goal, blocked_set)
        piece = Piece(initial, route, name, 0)
        pieces.append(piece)

    


def slide(curr_loc):
        slide_options = adjacents(curr_loc)
        return slide_options

#this will return adjacent hexes of a given hex
def adjacents(curr_loc):
    # FROM ZAKARYA: HOW DO WE MAKE SURE THEY ON THE BOARD? 
    adjacents = []
    adjacents.append(curr_loc.r + 1, curr_loc.q)
    adjacents.append(curr_loc.r + 1, curr_loc.q + 1)
    adjacents.append(curr_loc.r - 1, curr_loc.q)
    adjacents.append(curr_loc.r - 1, curr_loc.q - 1)
    adjacents.append(curr_loc.r, curr_loc.q + 1)
    adjacents.append(curr_loc.r, curr_loc.q - 1)
    return adjacents
            
#this will return a list of possible hexes for swing action
# def swing(curr_loc, token_list):
#     swing_options = []
#     adj_list = adjacents(curr_loc) 
#     curr_piece  = Piece()
    
#     for (r,q) in token_list:
#             curr_piece.r = r
#             curr_piece.q = q
            
#             if (curr_piece.r, curr_piece.q) in adj_list:
#                 for hex in adjacents(curr_piece):
#                     swing_options.append(hex)   
#     return swing_options
            
def move(curr_loc, next_loc):
    slide_options = slide(curr_loc)
    swing_options = swing(curr_loc, player_pieces)
    
    if next_loc in swing_options:  # first check the swing as it maybe overlab with slide
        print_swing(curr_loc.r, curr_loc.q, next_loc.r, next_loc.q)
    else:
        print_swing(curr_loc.r, curr_loc.q, next_loc.r, next_loc.q)
        #don't forget to pop out the item from the movement list so next time this function will check the next move
        
    
    
def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            # Stores all the pieces
            pieces = [] 
            blocked_set = make_blocked(data['block'])
            upper_pieces = make_dict(data['upper'])
            lower_pieces = make_dict(data['lower'])
            
            # Sorting assuming that low pieces are closest to low pieces
            sort_pieces(upper_pieces)
            sort_pieces(lower_pieces)

            # Gets the routes of all 3 kinds of pieces and stores them in moves
            get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 's', 'p')
            get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 'r', 's')
            get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 'p', 'r')
            # JUST GOTTA MAKE SURE THEY DONT COLLIDE

            # HAVE THESE FOR REFERENCE FOR NOW 
            # [(1, -1), (0, -1), (-1, 0), (-1, 1)]
            # [(-3, 2), (-2, 1), (-1, 0), (0, -1), (1, -1)]
            pairs = {'s': 'p', 'p' : 'r', 'r' : 's'}
            
            turn = 0
            running = True
            # We remove at the end so that we dont disturb any loops
            remove_index = [] 
            while(running):
                # Go through all pieces
                for i in range(0, len(pieces)): 
                    piece = pieces[i]
                    moves = piece.movements
                    # If we have reached goal means we no longer need to print so we add it 
                    # to indexes that need to be removed
                    if (len(moves) - 1 == piece.index):
                        target = pairs[piece.name]
                        if (len(lower_pieces[target]) > 0): 
                            turn -= 1
                            remove_index.append(i)
                            get_new_route(pieces, piece.current, lower_pieces, piece.name, target, blocked_set)
                        else: 
                            remove_index.append(i)
                    else:
                        p = moves[piece.index]
                        p2 = moves[piece.index+1]
                        print_slide(turn, p[0], p[1], p2[0], p2[1])
                        # Update the Pieces current position 
                        piece.current = p2
                    piece.index += 1
                turn += 1
                    
                # Check after loop if any indexes need to be removed and remove them
                if len(remove_index) > 0: 
                    for i in remove_index: 
                        pieces.pop(i)
                        remove_index.pop()
                # If theres no more pieces left we exit 
                if len(pieces) == 0: 
                    running = False
                
             

                #implement the movements for all the pieces
                #print the slide and swing actions and popo out the item from the list after each movement
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
    
    
    
    # DONT FORGET THESE
    # If the hex is occupied by one or more tokens with each symbol,all of the tokens are defeated.
    # If the hex is occupied by a Rock token, all Scissors tokens there are defeated.
    # If the hex is occupied by a Scissors token, all Paper tokens there are defeated.
    # If the hex is occupied by a Paper token, all Rock tokens there are defeated.
