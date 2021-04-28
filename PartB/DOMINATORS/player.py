from DOMINATORS.board import Board
from DOMINATORS.piece import Piece
from random import randrange
from DOMINATORS.node import Node

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here 

        # If upper is given to us we can start with x = 4 and y is anything in the given range
        if player == "upper": 
            self.start = (4, 0)
            self.move = "SUBTRACT"
        else: 
            self.start = (-4, 0)
            self.move = "ADD"
        
        self.player_type = player
        self.board = Board()
        self.turn = 0 
        self.first_turn = True 
        self.throws = 0 
        
    def estimate(self, our, opponent):
        if our in self.board.opponents:
            return 1
        elif opponent in self.board.our_pieces: 
            return - 1
        else: 
            return 0 


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # if self.player_type == "lower":
        # Need to make sure killed pieces dont exist 
        token = ["r", "s", "p"]
        sent = False
        # ALSO NEED TO MAKE SURE THROWS DONT EXCEED 9 


        # So if in thhe same turn a piece is killed without 
        # update being called we get erorr 

        # put your code here
        # How to decide whether to throw or slide 
        if self.turn % 2 ==  0 and self.first_turn: 
            self.first_turn = False
            # self.turn += 1
            r_index = randrange(len(token))
            self.throws += 1
            sent = True
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif self.turn % 2 ==  0 and self.throws < 10: 
            # How to calculate new throw position
            self.turn += 1
            self.throws += 1
            if (self.move == "ADD"):
                new = (self.start[0] + 1, self.start[1])
                if new in self.board.spots: 
                    sent = True
                    self.start = new
            else: 
                new =  self.start = (self.start[0] - 1, self.start[1])
                if new in self.board.spots:
                    sent = True 
                    self.start = new

            r_index = randrange(len(token))
            # print("AAAAAAAAAAAAAAAAAAAAA")
            # print(self.throws)
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif not sent: 
            self.turn += 1
            random_index = randrange(len(self.board.our_pieces))
            to_move = self.board.our_pieces[random_index]
            target = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
            print(f'select = {to_move.current}')
            
            for t in target: 
               
                movex = t[0] + to_move.current[0] 
                movey = t[1] + to_move.current[1] 
                # print("AA")
                if (movex, movey) in self.board.spots: 
                    move = (movex, movey)
                    print(move)

                    return ("SLIDE", to_move.current, move)
          
        #     # Get one piece from our list 
        #     # Perform minimax 
        #     # And slide towards best possible outcome 
        #     # Q : Did we wanna loop through and perform MM on each or just choose random? 
        #     # Q: and how to choose which opponent piece to target? 
            # random_index = randrange(len(self.board.our_pieces))
            # to_move = self.board.our_pieces[random_index]
            # Perform MM


     

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        # Means its a throw 
        battle = False
        p = None
        o = None

        # print(f'{player_action[2]}   {opponent_action[2]}')
        if player_action[2] == opponent_action[2]: 
            battle = True

        if opponent_action[0] == "THROW": 
            opp_piece = Piece(opponent_action[2], opponent_action[1]) 
            o = opp_piece
            self.board.opponents.append(opp_piece)  
        else: 
            old_location = opponent_action[1]
            # print("SLIDE opp")
            # Searching for which piece had that initial location
            for piece in self.board.opponents: 
                # print("FOUND WHICH PIECE FOR OPP")
                # If location matches we update its position
                if piece.current == old_location: 
                    # print("CHASNGED OPP") 
                    piece.current = opponent_action[2] 
                    # print(piece.current)
                    o = piece
                    break 

        # Also need to make sure killed pieces dissapear
        # Make sure upper chooses upper  

        if player_action[0] == 'THROW': 
            p_piece =  Piece(player_action[2], player_action[1])  
            p = p_piece 
            self.board.our_pieces.append(p_piece)
        else: 
            old_location = player_action[1]
            # print("SLIDE")
            # Searching for which piece had that initial location
            for piece in self.board.our_pieces: 
                # print("FOUND WHICH PIECE")
                # If location matches we update its position
                if piece.current == old_location:  
                    piece.current = player_action[2]
                    # print("--------------------")
                    # print(piece.current) 
                    p = piece
        
        print(len(self.board.our_pieces))
        print(len(self.board.opponents))

        # For any current battles 
        if battle: 
            print("battled")
            if p.name == "r" and o.name == "s" or p.name == "p" and o.name == "r" or p.name == "s" and o.name == "p" :
                print("P1")
                ind = self.board.opponents.index(o)
                self.board.opponents.pop(ind)
                battle = False
            elif o.name == "r" and p.name == "s" or o.name == "p" and p.name == "r" or o.name == "s" and p.name == "p":
                print("p2")
                ind = self.board.our_pieces.index(p)
                self.board.our_pieces.pop(ind)
                battle = False

        # FOR BATTLE WE CHECKED CURRENT PIECE NOT PREVIUS PIECEDS 
        # Loop through opponent and our pieces to see if anything was killed in battle 
        for pie in self.board.our_pieces:
            if opponent_action[2] == p.current: 
                # Battle and remove 
                print("battled")
                if pie.name == "r" and o.name == "s" or pie.name == "p" and o.name == "r" or pie.name == "s" and o.name == "p" :
                    print("P1")
                    ind = self.board.opponents.index(o)
                    self.board.opponents.pop(ind)
                    # battle = False
                elif o.name == "r" and pie.name == "s" or o.name == "p" and pie.name == "r" or o.name == "s" and pie.name == "p":
                    print("p2")
                    ind = self.board.our_pieces.index(pie)
                    self.board.our_pieces.pop(ind)
                    # battle = False

            # Our piece may kill itself 
            if player_action[2] == pie.current: 
                # Battle and remove 
                print("battled")
                if pie.name == "r" and p.name == "s" or pie.name == "p" and p.name == "r" or pie.name == "s" and p.name == "p" :
                    print("P1")
                    ind = self.board.opponents.index(o)
                    self.board.opponents.pop(ind)
                    # battle = False
                elif p.name == "r" and pie.name == "s" or p.name == "p" and pie.name == "r" or p.name == "s" and pie.name == "p":
                    print("p2")
                    ind = self.board.our_pieces.index(p)
                    self.board.our_pieces.pop(ind)

     






