from DOMINATORS.piece_state import PieceState

class Board:
    def __init__(self): 
        # List of piece classes
        self.our_pieces = [] 
        self.our_locations = [] 
        self.opponents = [] 
        self.opp_locations = []
        self.spots = self.initilaise_board()
        self.max_depth = 4
        self.vectors = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
        self.winning_positions = []
        self.get_winning_position()
        

    def initilaise_board(self): 
        spots = set() 
        row = 4 
        r = 4
        rbottom = -4 

        while True:
            q = -4 
            qbottom = 4 
            for _ in range(0, row + 1): 
                # state = PieceState("", (r, q), "")
                # state2 = PieceState("", (rbottom, qbottom), "")
                spots.add((r, q))
                spots.add((rbottom, qbottom))
                q += 1
                qbottom -= 1

            r -= 1
            rbottom += 1
            row += 1
            if row == 9: 
                return spots