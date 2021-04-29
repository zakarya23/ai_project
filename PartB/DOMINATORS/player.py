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

    def check_piece(self, position):
        # print("aaaa")
        for opp in self.board.opponents: 
            if position.current == opp.current: 
                # print('battled')
                if position.name == "r" and opp.name == "s" or position.name == "p" and opp.name == "r" or position.name == "s" and opp.name == "p":
                    # print("haha")
                    return 1
                    # ind = self.board.opponents.index(p2)
                    # self.board.opponents.pop(ind)
                elif opp.name == "r" and position.name == "s" or opp.name == "p" and position.name == "r" or opp.name == "s" and position.name == "p":
                    # print("p2")
                    return -1
                    # ind = self.board.our_pieces.index(p1)
                    # self.board.our_pieces.pop(ind) 

            for opp in self.board.our_pieces: 
                # print(opp.name)
                if position.current == opp.current: 
                    # print('battled')
                    if position.name == "r" and opp.name == "s" or position.name == "p" and opp.name == "r" or position.name == "s" and opp.name == "p":
                        # print("haha")
                        return 1
                        # ind = self.board.opponents.index(p2)
                        # self.board.opponents.pop(ind)
                    elif opp.name == "r" and position.name == "s" or opp.name == "p" and position.name == "r" or opp.name == "s" and position.name == "p":
                        # print("p2")
                        return -1
        return 0 
        
    def minimax(self, current_piece, depth, maximising):
        if depth == 0: 
            # Evaluation function
            # print("pop")
            # future_piece = Piece()
            return self.check_piece(current_piece)
        children = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
        future_piece = None
        if maximising: 
            highest = -(1000000000 * 100000000)
            for c in children: 
                child = (current_piece.current[0] + c[0], current_piece.current[1] + c[1])
                if child in self.board.spots:
                    future_piece = Piece(child, current_piece.name)
                    score = self.minimax(future_piece, depth - 1, False)
                    # if score > 0:
                    # print(f'{current_piece.current} == {child}  {score}')
                   
            highest = max(highest, score[1])
            # print("highest")
            return (future_piece, highest)
        else: 
            lowest = (1000000000 * 100000000)
            for c in children: 
                child = (current_piece.current[0] + c[0], current_piece.current[1] + c[1])
                if child in self.board.spots:
                    future_piece = Piece(child, current_piece.name)
                    score = self.minimax(future_piece, depth - 1, True)
                    # print("OPOPO")
                    print(f'score = {score[1]}')
            lowest = min(lowest, score[1])
            return (future_piece, lowest)

    def best_move(self): 
        highest = -(1000000000 * 100000000)
        piece = None
        for p in self.board.our_pieces: 
           new_score = self.minimax(p, 5, True)
           if new_score > highest: 
               highest = new_score
               piece = p
        return (piece, highest)
        
    # def estimate(self, our, opponent):
    #     if our in self.board.opponents:
    #         return 1
    #     elif opponent in self.board.our_pieces: 
    #         return - 1
    #     else: 
    #         return 0 

    def throw(self, sent): 
        token = ["r", "s", "p"]
        self.turn += 1
        self.throws += 1
        if (self.move == "ADD"):
            new = (self.start[0] + 1, self.start[1])
            if new in self.board.spots and new not in self.board.our_locations: 
                sent = True
                self.start = new
        else: 
            new =  self.start = (self.start[0] - 1, self.start[1])
            if new in self.board.spots and new not in self.board.our_locations:
                sent = True 
                self.start = new

        r_index = randrange(len(token))
        # print("AAAAA")    
        if sent:
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        token = ["r", "s", "p"]
        sent = False

        # put your code here
        # How to decide whether to throw or slide 
        if self.turn % 2 ==  0 and self.first_turn: 
            self.first_turn = False
            # self.turn += 1
            r_index = randrange(len(token))
            self.throws += 1
            sent = True
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif self.turn % 2 ==  0 and self.throws < 9: 
            # How to calculate new throw position
            token = ["r", "s", "p"]
            self.turn += 1
            self.throws += 1
            if (self.move == "ADD"):
                new = (self.start[0] + 1, self.start[1])
                if new in self.board.spots and new not in self.board.our_locations: 
                    sent = True
                    self.start = new
            else: 
                new =  self.start = (self.start[0] - 1, self.start[1])
                if new in self.board.spots and new not in self.board.our_locations:
                    sent = True 
                    self.start = new

            r_index = randrange(len(token))
            # print("AAAAA")
            if sent:
                return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        while not sent: 
            self.turn += 1
    
            # RETURN PIECE AND WHICH WAY TO MOVE 
            piece = self.best_move()
            print("POPOPOPO")
            print(piece)
            
            
            to_move = piece[0] 
            move = piece[1] 

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
        o = None
        p = None

        if opponent_action[0] == "THROW": 
            opp_piece = Piece(opponent_action[2], opponent_action[1]) 
            self.board.opponents.append(opp_piece)  
            
            o = opp_piece
        else: 
            old_location = opponent_action[1]
            # Searching for which piece had that initial location
            for piece in self.board.opponents: 
                # If location matches we update its position
                if piece.current == old_location: 
                    piece.current = opponent_action[2] 
                    o = piece
                    break 

        if player_action[0] == 'THROW': 
            p_piece =  Piece(player_action[2], player_action[1])  
            self.board.our_pieces.append(p_piece)
            self.board.our_locations.append(player_action[2])
            p = p_piece
        else: 
            old_location = player_action[1]

            # Searching for which piece had that initial location
            for piece in self.board.our_pieces: 

                # If location matches we update its position
                if piece.current == old_location: 
                    i = self.board.our_locations.index(piece.current)
                    self.board.our_locations.pop(i)
                    piece.current = player_action[2]
                    self.board.our_locations.append(piece.current)
                    p = piece
                    break

        def verse(self, p1, p2): 
            print("battled")
            if p1.name == "r" and p2.name == "s" or p1.name == "p" and p2.name == "r" or p1.name == "s" and p2.name == "p":
                print("p1")
                ind = self.board.opponents.index(p2)
                self.board.opponents.pop(ind)
            elif p2.name == "r" and p1.name == "s" or p2.name == "p" and p1.name == "r" or p2.name == "s" and p1.name == "p":
                print("p2")
                ind = self.board.our_pieces.index(p1)
                self.board.our_pieces.pop(ind) 

        # Checking if something was thrown onto my pieces 
        for p in self.board.our_pieces: 
            if p.current == opponent_action[2]:
                print("battled!")
                if p.name == "r" and o.name == "s" or p.name == "p" and o.name == "r" or p.name == "s" and o.name == "p":
                    print("p1")
                    o.status = False
                    # ind = self.board.opponents.index(o)
                    # self.board.opponents.pop(ind)
                elif o.name == "r" and p.name == "s" or o.name == "p" and p.name == "r" or o.name == "s" and p.name == "p":
                    print("p2")
                    p.status = False
                    # ind = self.board.our_pieces.index(p)
                    # self.board.our_pieces.pop(ind) 
            # if opponent_action[0] == "SLIDE" and p.current == opponent_action[2]:

        # Check if we hurt enemey 
        for o in self.board.opponents: 
            if o.current == player_action[2] and p in self.board.our_pieces: 
                print("battled!")
                if p.name == "r" and o.name == "s" or p.name == "p" and o.name == "r" or p.name == "s" and o.name == "p":
                    print("p1")
                    o.status = False
                    # ind = self.board.opponents.index(o)
                    # self.board.opponents.pop(ind)
                elif o.name == "r" and p.name == "s" or o.name == "p" and p.name == "r" or o.name == "s" and p.name == "p":
                    print("p2")
                    p.status = False
                    # ind = self.board.our_pieces.index(p)
                    # self.board.our_pieces.pop(ind) 

        # We killed ourself 
        for pie in self.board.our_pieces: 
            if pie.current == player_action[2]:
                print("battled SAME ME")
                if pie.name == "r" and p.name == "s" or pie.name == "p" and p.name == "r" or pie.name == "s" and p.name == "p":
                    print("p1")
                    # ind = self.board.our_pieces.index(p)
                    # self.board.our_pieces.pop(ind)
                    p.status = False
                elif p.name == "r" and pie.name == "s" or p.name == "p" and pie.name == "r" or p.name == "s" and pie.name == "p":
                    print("p2")
                    # ind = self.board.our_pieces.index(p)
                    # self.board.our_pieces.pop(ind) 
                    pie.status = False

        # opp killed itself
        for opp in self.board.opponents: 
            if opp.current == opponent_action[2] and o in self.board.opponents:
                print("battled SAME")
                if opp.name == "r" and o.name == "s" or opp.name == "p" and o.name == "r" or opp.name == "s" and o.name == "p":
                    print("p1")
                    o.status = False
                    # ind = self.board.opponents.index(o)
                    # self.board.opponents.pop(ind)
                elif o.name == "r" and opp.name == "s" or o.name == "p" and opp.name == "r" or o.name == "s" and opp.name == "p":
                    print("p2")
                    opp.status = False
                    # ind = self.board.opponents.index(o)
                    # self.board.opponents.pop(ind)
