

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

    #implementation of the swing movement goes here
    # def swing(curr.position):
       
    #    return None

    #implementation of the slide movement goes here
    # def slide(curr.position):

    #     return None