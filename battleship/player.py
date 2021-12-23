from typing import Tuple, List

from battleship.board import Board
from battleship.ship import Ship


class Player:
    def __init__(self):
        self.board: Board = Board()
        self.hits = []
        self.ships: List[Ship] = []
        self.guesses: List[Tuple[int, int]] = []

    def lost(self):
        return len(self.ships) == 0

    def add_guess(self, guess: Tuple[int, int]):
        self.guesses.append(guess)

    def get_guess(self):
        return self.guesses

    def in_guesses(self, guess: Tuple[int, int]):
        return guess in self.guesses

    def hit_slot(self, slot: Tuple[int, int]):
        row, col = slot
        if self.board.hit_slot(row, col):
            for ship in self.ships.copy():
                if slot in ship.get_slots():
                    ship.hit_slot(slot)
            return True
        else:
            return False

    def remove_ship(self, ship: Ship):
        self.ships.remove(ship)

    def add_ship(self, ship: Ship):
        if self.board.check_ship_slots(ship):
            self.board.place_ship(ship)
            self.ships.append(ship)

    def add_hit(self, hit: Tuple[int, int]):
        self.hits.append(hit)

    def print_board(self):
        self.board.print_board()

    def get_ships(self):
        return self.ships
