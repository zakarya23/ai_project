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
        else: 
            self.start = (-4, 0)
        
        self.player_type = player
        self.board = Board()
        self.turn = 0 
        self.first_turn = True 
        

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # if self.player_type == "lower":
        token = ["r", "s", "p"]
    

        # put your code here
        # How to decide whether to throw or slide 
        if self.turn % 2 ==  0 and self.first_turn: 
            self.first_turn = False
            # self.turn += 1
            r_index = randrange(len(token))
            
            return ("THROW", token[r_index], (self.start[0], self.start[1])) 
        elif self.turn % 2 ==  0: 
            # How to calculate new throw position
            self.turn += 1
            return ("THROW", "s", (self.start[0], self.start[1])) 
        else: 
            self.turn += 1
            random_index = randrange(len(self.board.our_pieces))
            to_move = self.board.our_pieces[random_index]
            target = [(0,1),(0,-1),(1,-1),(1,0),(-1,0),(-1,1)]
            
            for t in target: 
               
                movex = t[0] + to_move.current[0] 
                movey = t[1] + to_move.current[1] 
                if (movex, movey) in self.board.spots: 
                    move = (movex, movey)
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
        if opponent_action[0] == "THROW": 
            opp_piece = Piece(opponent_action[2], opponent_action[1]) 
            self.board.opponents.append(opp_piece)  
        else: 
            old_location = opponent_action[1]
            # Searching for which piece had that initial location
            for piece in self.board.opponents: 
                # If location matches we update its position
                if piece.current == old_location:  
                    piece.current = opponent_action[2] 

        if player_action[0] == 'THROW': 
            p_piece =  Piece(player_action[2], player_action[1])   
            self.board.our_pieces.append(p_piece)
        else: 
            old_location = player_action[1]
            # Searching for which piece had that initial location
            for piece in self.board.our_pieces: 
                # If location matches we update its position
                if piece.current == old_location:  
                    piece.current = player_action[2] 