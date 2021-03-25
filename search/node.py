

class Node():
    def init(self, parent=None, initial=None, goal=None):
        if parent:
            self.parent = parent
        self.inital = initial
        self.goal = goal 
        self.type = None   #paper,rock etc.
        self.g = 0
        self.h = 0
        self.f = 0

    #implementation of the slide movement goes here, the current position of the node + the direction of the
    # movement(left, right, lower_left,lower_right, upper_right, nupper_left) 
 
     def slide(node.position, direction):
        
       # movement of one tile towards the given direction like (x+1,y) or (x, y-1), we have 6 different movements
       if (direction == "L"):
             curr.position[0] - 1;
             curr.position[1];
            
       if (direction =="R"):
             curr.position[0] + 1;
             curr.position[1];
       
       if (direction =="UR"):
             curr.position[0] + 1;
             curr.position[1] + 1;
            
       if (direction =="UL"):
             curr.position[0] - 1;
             curr.position[1] + 1;
    
       if (direction =="LR"):
             curr.position[0] + 1;
             curr.position[1] - 1;
            
       if (direction =="LL"):
             curr.position[0] - 1;
             curr.position[1] - 1;
         
            
            
        return curr;

    #implementation of the swing movement goes here 
    #the current positon, direction of the movement
    #this will return a list of possible hexes for swing action
    
    #this will return adjacent hexes of a given hex
    def adjacents(node.position):
        adjacents = []
        
        adjacents.append(node.position[0] + 1; node.position[1]);
        adjacents.append(node.position[0] + 1; node.position[1] + 1);
        adjacents.append(node.position[0] - 1; node.position[1]);
        adjacents.append(node.position[0] - 1; node.position[1] - 1);
        adjacents.append(node.position[0]; node.position[1] + 1);
        adjacents.append(node.position[0]; node.position[1] - 1);
        
        return adjacents;
        
        
    
    
    
    #this will return a list of possible hexes for swing action
    def swing(node.position, token_list):
        move_list =[]
        curr_node  = Node()
              
              for (r,q) in token_list:
                    curr_node.position[0] = r;
                    curr_node.position[0] = q;
                    
                    for hex in adjacents(curr_node.position):
                        move_list.append(hex);
                        
                    
                    
              
        return move_list; #then we can check the hexes in the list with our shortest path and decide on the movement.
                          #if one of the swings option is in shortest path => move there
        
              
    def print_mode(turn, curr_position, next_position, type): #type = either slide or swing
        if type == "slide":
            print("Turn" + turn "SLIDE from" %curr_position + "to" + %next_psotion);
            
        if type == "swing":
            print("Turn" + turn "SWING from" %curr_position + "to" + %next_psotion);
            
                    
                    # Both Scissors now share a hexTurn 2: SLIDE from (1,-1) to (0,-1)
        
        
       
    # it should move to one of the adjacent hexes of the chosen same player's token 
    

    #     return None
