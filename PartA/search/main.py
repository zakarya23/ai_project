"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Authors: Zakarya & Kamyar
Group: DOMINATORS
"""
import sys
import json
from search.util import print_board, print_slide, print_swing
from search.piece import Piece
from search.changes import get_routes, get_new_route, future_directions, initialise_routes
from search.changes import get_new_random, random_route, make_solution
from search.construct import all_goals, format_input, make_dict, make_blocked, sort_pieces
from search.changes import run_search

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            # Will be storing all the pieces we start of with 
            pieces = [] 
            # Our pieces, opponents pieces, blocked pieces, and all the ones we need to kill. 
            upper_pieces, lower_pieces, blocked_set, to_kill = format_input(data)
            # Gets the routes of all 3 kinds of pieces and stores them in moves
            initialise_routes(upper_pieces, lower_pieces, pieces, blocked_set)
            # Run the algorithm
            run_search(pieces, to_kill, lower_pieces, blocked_set)

    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)
