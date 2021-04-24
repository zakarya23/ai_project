from DOMINATORS.board import Board
from DOMINATORS.piece import Piece

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

        # print(self.start)
        self.player_type = player
        self.board = Board()
        self.turn = 0 
        

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        if self.turn % 2 ==  0: 
            self.turn += 1
            return ("THROW", "s", (self.start[0], self.start[1]))
        elif self.turn % 2 == 1:  
            self.turn += 1
            return ("THROW", "r", (self.start[0], self.start[1]))
        # else:
        #     if self.player_type == "upper":
        #         return ("SLIDE", (self.start[0], self.start[1]), (3, 0))
        #     else: 
        #         return ("SLIDE", (self.start[0], self.start[1]), (-3, 0))



    
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
        else: 
            opp_piece = Piece(opponent_action[2], opponent_action[1])

        self.board.opponents.append(opp_piece)
        self.board.our_pieces.append(player_action)
        print(self.board.opponents)
    
        

