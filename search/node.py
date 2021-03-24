

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
    # movement(left, right, south_left,south_right, north_right, north_left) 
 
    # def slide(curr.position, direction):
       # movement of one tile towards the given direction like (x+1,y) or (x, y-1), we have 6 different movements
       
    #    return None

    #implementation of the swing movement goes here 
    #the current positon, direction of the movement
    
    # def swing(curr.position, direction, list of same player's tokens):
    
    # it should move to one of the adjacent hexes of the chosen same player's token 
    

    #     return None
