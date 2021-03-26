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

def get_routes(upper, lower, moves, blocked_set, initial, target): 
    if initial not in upper or target not in lower: 
        return None
    initials = upper[initial]
    for piece in initials: 
        p = lower[target]
        goal = None
        if len(p) > 0:
            goal = p.pop()
            initials.pop()
        if goal: 
            route = make_solution(piece, goal, blocked_set)
            moves[piece] = route

            
def move(curr_loc, next_loc):
    slide_options = slide(curr_loc);
    swing_options = swing(curr_loc, player_pieces);
    
    if next_loc in swing_otpions:
        print_swing(curr_loc.r, curr_loc.q, next_loc.r, next_loc.q);
    
    esle:
        print_swing(curr_loc.r, curr_loc.q, next_loc.r, next_loc.q);
        
        #don't forget to pop out the item from the movement list so next time this function will check the next move
        
    
    
def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            moves = {}
            blocked_set = make_blocked(data['block'])
            upper_pieces = make_dict(data['upper'])
            lower_pieces = make_dict(data['lower'])
            
            # Sorting assuming that low pieces are closest to low pieces
            sort_pieces(upper_pieces)
            sort_pieces(lower_pieces)

            # Gets the routes of all 3 of our pieces and stores them in moves
            get_routes(upper_pieces, lower_pieces, moves, blocked_set, 's', 'p')
            get_routes(upper_pieces, lower_pieces, moves, blocked_set, 'r', 's')
            get_routes(upper_pieces, lower_pieces, moves, blocked_set, 'p', 'r')
            # JUST GOTTA MAKE SURE THEY DONT COLLIDE
            print(moves)
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
