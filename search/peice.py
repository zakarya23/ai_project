class Piece:
    def __init__(self, r=0, q=0):
        self.r = r
        self.q = q

    def distance_from_origin(self):
        return ((self.r ** 2) + (self.q ** 2)) ** 0.5

    def print_piece(self):
        print('({0}, {1})'.format(self.r, self.q))
