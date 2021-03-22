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


def make_solution(inital, goal): 
    unvisited = PriorityQueue()
    visited = [] 
    # Format is [(x, y), distance]
    start = [0, (inital[0], inital[1])]
    unvisited.put(start)
    not_found = True

    while not unvisited.empty() and not_found: 
        current = unvisited.get(0)
        for next_position in [(0, 1), (1, 0), (-1, 0), (0, -1)]: 

            new_point = (current[1][0] + next_position[0], current[1][1] + next_position[1])
            if (new_point == goal): 
                not_found = False
                break
            distance_to_goal = math.sqrt(abs(goal[0] - new_point[0]) + abs(goal[1] - new_point[1]))
            unvisited.put([distance_to_goal, (new_point)])
        visited.append(current)

    # Will give final path to follow
    visited.append(goal)
    print((visited))


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            # print(data)
            print("got in")
            initials = data['upper']
            goals = data['lower']
            blocked = data['block']
            make_solution((0, 0), (2,4))
            # print(initials)   
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).