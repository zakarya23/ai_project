class Utility: 
    def check_piece_future(self, location, opponent_pieces, piece):
        pairs = {'r':'s', 'p': 'r', 's':'p'} 
        if (location in opponent_pieces) and (len(opponent_pieces[location]) > 0): 
            opp = opponent_pieces[location][0]
            if pairs[opp] == piece:
                return -1 
            elif pairs[piece] == opp:
                return 1