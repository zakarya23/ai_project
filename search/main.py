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

def random_route(point, blocked_set, pieces): 
    target = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
    route = [] 
    route.append(point)
    R_RANGE = (-4, 4)
    Q_RANGE = (-4, 4)
    for next_position in target: 
        new_point = (point[0] + next_position[0], point[1] + next_position[1]) 
        if new_point in blocked_set or (new_point[0] > R_RANGE[1]) or (new_point[0] < R_RANGE[0]) or (new_point[1] > Q_RANGE[1]) or (new_point[1] < Q_RANGE[0]): 
            continue
        else: 
            route.append(new_point)
    return sorted(route)


def get_routes(upper, lower, pieces, blocked_set, initial, target):
    if initial not in upper and target not in lower: 
        return None 
    elif target not in lower: 
        points = upper[initial]
        # Find any adjecent block that isnt blocked or taken and then move it there. 
        for p in points: 
            route = random_route(p, blocked_set, pieces)
            # goal = route[-1]
            piece = Piece(p, route, initial, 0)
            pieces.append(piece)
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
            
def get_new_route(turn, piece, lower_pieces, blocked_set):
    pairs = {'s': 'p', 'p' : 'r', 'r' : 's'}
    all_targets = lower_pieces[pairs[piece.name]]
    # print(all_targets)
    goal = None
    if len(all_targets) > 0:
        goal = all_targets.pop()
        # initials.pop()
    if goal: 
        route = make_solution(piece.current, goal, blocked_set)
        piece.current = route.pop(0)
        second = route[0]
        print_slide(turn, piece.current[0], piece.current[1], second[0], second[1])
        piece.current = second
        piece.movements = route
        return None

def all_goals(goals): 
    '''
    Stores all the pieces we need to kill 
    '''
    targets = [] 
    for goal in goals: 
        targets.append((goal[1], goal[2]))
    return targets 

def future_directions(turn, piece, pieces, lower_pieces, blocked_set, to_kill):
    pairs = {'s': 'p', 'p' : 'r', 'r' : 's'}
    if pairs[piece.name] not in lower_pieces: 
        # Make random route for the piece 
        get_new_random(turn, pieces, piece, blocked_set)
        return None
    else:
        if (piece.current in to_kill):
            # print("KIL") SHOULDVE FINISHED ON 12 
            # print("KIL")
            index = to_kill.index(piece.current)
            to_kill.pop(index)
        target_pieces = lower_pieces[pairs[piece.name]]
        if len(target_pieces) > 0: 
            # Means still more pieces to target 
            get_new_route(turn, piece, lower_pieces, blocked_set)
            return None 
        elif len(to_kill) == 0: 
            return None
        else: 
            # No targets left so random movement
            get_new_random(turn, pieces, piece, blocked_set)
            return None

    return None

def initialise_routes(upper_pieces, lower_pieces, pieces, blocked_set): 
    # Sorting assuming that low pieces are closest to low pieces
    sort_pieces(upper_pieces)
    sort_pieces(lower_pieces)
    get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 's', 'p')
    get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 'r', 's')
    get_routes(upper_pieces, lower_pieces, pieces, blocked_set, 'p', 'r')

# CHANGED
def get_new_random(turn, pieces, piece, blocked_set):
    route = random_route(piece.current, blocked_set, pieces)
    piece.current = route.pop(0)
    second = route[0]
    print_slide(turn, piece.current[0], piece.current[1], second[0], second[1])
    piece.current = second
    piece.movements = route
    return None

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            R_RANGE = (-4, 4)
            Q_RANGE = (-4, 4)
            pieces = [] 
            blocked_set = make_blocked(data['block'])
            upper_pieces = make_dict(data['upper'])
            lower_pieces = make_dict(data['lower'])
            to_kill = all_goals(data['lower'])
            # print(lower_pieces)
            # Gets the routes of all 3 kinds of pieces and stores them in moves
            initialise_routes(upper_pieces, lower_pieces, pieces, blocked_set)
            # print(lower_pieces)
            # JUST GOTTA MAKE SURE THEY DONT COLLIDE
            pairs = {'s': 'p', 'p' : 'r', 'r' : 's'}
            turn = 1
            running = True
            # We remove at the end so that we dont disturb any loops
            remove_index = []
            i = 0 
            while(running):
                for piece in pieces: 
                    movements = piece.movements
                    if len(to_kill) == 0: 
                        running = False
                        break

                    if (len(movements) == 1):
                        point = movements[0]
                        piece.current = point
                        # Make new route for it based on whether it has any more targets 
                        # print("P")
                        future_directions(turn, piece, pieces, lower_pieces, blocked_set, to_kill)
                        # print("A")
                   
                    else: 
                        first = movements.pop(0)
                        next = movements[0]
                        print_slide(turn, first[0], first[1], next[0], next[1])
                        # EXCEPT OF NEXT IT SHOULD BE THE GOAL OF THE PIECE 
                        if next in to_kill: 
                            index = to_kill.index(next)
                            to_kill.pop(index) 
                        if len(to_kill) == 0: 
                            running = False
                            break     

                        piece.current = next

                    # movements.pop(0) 
                i += 1
                turn += 1

                
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)