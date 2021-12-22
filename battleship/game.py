from typing import List

from .board import Board
from .player import Player


class Game:
    def __init__(self, players: List[Player]):
        self._players = players
        self.current_player = 0

    def init_game(self):
        self.players_boards = [Board(), Board()]
        self.turn = 0

    def choose_fleet(self):
        pass
