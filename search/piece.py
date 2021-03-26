class Piece:
    def __init__(self, current, movements, name):
        self.current = current
        self.movements = movements
        self.name = name

    # def distance_from_origin(self):
    #     return((self.r_c ** 2) + (self.q_c ** 2)) ** 0.5

    # def print_piece(self):
    #     print('({0}, {1})'.format(self.r_c, self.q_c))
