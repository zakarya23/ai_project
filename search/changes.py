from search.util import print_board, print_slide, print_swing
from search.piece import Piece
from search.construct import sort_pieces
from queue import PriorityQueue
import math

def run_search(pieces, to_kill, lower_pieces, blocked_set): 
    turn = 1
    running = True
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
                future_directions(turn, piece, pieces, lower_pieces, blocked_set, to_kill)
            else: 
                first = movements.pop(0)
                next = movements[0]
                print_slide(turn, first[0], first[1], next[0], next[1]) 
                if next in to_kill: 
                    index = to_kill.index(next)
                    to_kill.pop(index) 
                if len(to_kill) == 0: 
                    running = False
                    break     
                piece.current = next
        turn += 1

def get_new_random(turn, pieces, piece, blocked_set):
    route = random_route(piece.current, blocked_set, pieces)
    piece.current = route.pop(0)
    second = route[0]
    print_slide(turn, piece.current[0], piece.current[1], second[0], second[1])
    piece.current = second
    piece.movements = route
    return None

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

##
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
            
def get_new_route(turn, piece, lower_pieces, blocked_set):
    pairs = {'s': 'p', 'p' : 'r', 'r' : 's'}
    all_targets = lower_pieces[pairs[piece.name]]
    # print(all_targets)
    goal = None
    if len(all_targets) > 0:
        goal = all_targets.pop()
    if goal: 
        route = make_solution(piece.current, goal, blocked_set)
        piece.current = route.pop(0)
        second = route[0]
        print_slide(turn, piece.current[0], piece.current[1], second[0], second[1])
        piece.current = second
        piece.movements = route
        return None

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