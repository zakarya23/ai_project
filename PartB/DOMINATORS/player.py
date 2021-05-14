from DOMINATORS.update import update_states
from DOMINATORS.board import Board
from DOMINATORS.action import take_action

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.
        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        self.board = Board()
        self.states = {"turn": 0, "first_turn": True, "throws": 0, "opponent_throws": 0, "throw_x": None, "player_type": player, "board": Board(), "max_depth": 3, "pairs":{'r':'s', 'p': 'r', 's':'p'}}

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        return take_action(self.states)
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        update_states(player_action, opponent_action, self.states)
