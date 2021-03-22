"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing
import search.node as Node



#This will return a list of tuples demonstrating the shortest path
def make_solution(board, start, goal):

    #initializing start and end nodes
    
    start = Node(None, start)
      
    start.g = start.h = start.f = 0
    goal = Node(None, goal)  
    goal.g = goal.h = goal.f = 0


    unvisited = []  #visited nodes
    visited = []    #unvisited nodes

    unvisited.append(start)

    while len(unvisited) > 0:

        curr = unvisited[0]
        curr_index = 0

        for index, _hex in enumerate(unvisited):    
            if _hex.f < curr.f:        
                curr = _hex
                curr_index = index
        
        unvisited.pop(curr_index)
        visited.append(curr)


        if curr == goal:
            route = []
            curr_hex = curr
            while curr_hex is not None:
                route.append(curr_hex.position)
                curr_hex = curr_hex.parent
            return path[::-1] #this will reversed the path cause we are going towards goal


            child_hexes = []

            for next_position in [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]:

                    hex_pos = (curr.position[0]+next_position[0], curr.position[1]+next_position[1])

                    # we need an if node here to check if the hex is not out of the board


                    # if board[hex_pos[0]]hex_pos[1]] != block_location : ?  to check if its not a block


                    new_hex = Node(curr, next_position) #new hex

                    child_hexes.append(new_hex)


            #now it is time to check the child hexes 

            for child in child_hexes:

                for visited_child in visited:
                    if child == visited_child:
                        continue

                
                child.g = curr.g + 1
                #euclidean distance between child and the goal hex  
                child.h = ((child.position[0] - goal.position[0]) ** 2) + ((child.position[1] - goal.position[1]) ** 2)
                child.f = child.g + child.h

                #if child hex is in the unvisited list
                for unvisited_hex in unvisited:
                    if child == unvisited_hex and child.g > unvisited_hex.g:
                        continue


                unvisited.append(child)




                


                        
def make_graphs(initial, goal): 
    graphs = []
    
    return graphs


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            print(data)
            initials = data['upper']
            goals = data['lower']
            blocked = data['block']
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
