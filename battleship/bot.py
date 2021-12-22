import random
from typing import Tuple

from battleship.board import Board
from battleship.constants import HORIZONTAL, VERTICAL, SHIPS_SIZES, FLEET_ONE, FLEET_TWO, FLEETS
from battleship.ship import Ship


def random_slot():
    return random.randint(0, 10), random.randint(0, 10)


def random_placement():
    row, column = random_slot()
    orientation = random.choice([HORIZONTAL, VERTICAL])
    return row, column, orientation


class Bot:
    def __init__(self):
        self.board = Board()
        self.guesses = []

    def place_ships(self):
        fleet = FLEETS[random.choice([FLEET_ONE, FLEET_TWO])]
        for ship_name, amount in fleet.items():
            while amount > 0:
                row, column, ship_orientation = random_placement()
                ship_size = SHIPS_SIZES[ship_name]
                ship_slots = []
                if ship_orientation is HORIZONTAL:
                    ship_slots = [(row, column + x) for x in range(ship_size)]
                elif ship_orientation is VERTICAL:
                    ship_slots = [(row + x, column) for x in range(ship_size)]

                ship = Ship(ship_name, ship_size, ship_slots)
                if self.board.check_ship_slots(ship):
                    self.board.place_ship(ship)
                    amount -= 1

    def print_board(self):
        self.board.print_board()

    def hit_slot(self, row, col):
        return self.board.hit_slot(row, col)

    def lost(self):
        return self.board.lost()

    def random_hit(self):
        slot = random_slot()
        if slot in self.guesses:
            return self.random_hit()
        return slot

    def guess(self):
        return self.random_hit()


class SmartBot(Bot):
    def __init__(self):
        super(SmartBot, self).__init__()
        self.hits = []
        self.slots_scores = [[0]*10 for _ in range(10)]

    def add_hit(self, hit: Tuple[int, int]):
        self.hits.append(hit)

    def calc_scores(self):
        for row, col in self.hits:
            self.slots_scores[row][col] = -1

        for row, col in self.guesses:
            if not (row, col) in self.hits:
                self.slots_scores[row][col] = -2

        for row in range(10):
            for col in range(10):
                if self.slots_scores[row][col] == -1 or self.slots_scores[row][col] == -2:
                    continue

                if self.check_across(row, col):
                    self.slots_scores[row][col] = 5

                if self.check_diagonal(row, col):
                    self.slots_scores[row][col] = -2

    def check_diagonal(self, row, col):
        return (0 <= row - 1 < 10 and 0 <= col - 1 < 10 and self.slots_scores[row - 1][col - 1] == -1) or \
                (0 <= row - 1 < 10 and 0 <= col + 1 < 10 and self.slots_scores[row - 1][col + 1] == -1) or \
                (0 <= row + 1 < 10 and 0 <= col - 1 < 10 and self.slots_scores[row + 1][col - 1] == -1) or \
                (0 <= row + 1 < 10 and 0 <= col + 1 < 10 and self.slots_scores[row + 1][col + 1] == -1)

    def check_across(self, row, col):
        return (0 <= row - 1 < 10 and 0 <= col < 10 and self.slots_scores[row - 1][col] == -1) or \
               (0 <= row < 10 and 0 <= col + 1 < 10 and self.slots_scores[row][col + 1] == -1) or \
               (0 <= row + 1 < 10 and 0 <= col + 1 < 10 and self.slots_scores[row + 1][col] == -1) or \
               (0 <= row < 10 and 0 <= col - 1 < 10 and self.slots_scores[row][col - 1] == -1)

    def get_highscores(self):
        highscores = []
        for row in range(10):
            for col in range(10):
                if self.slots_scores[row][col] == 5:
                    highscores.append((row, col))
        return highscores

    def guess(self):
        if not self.hits:
            slot = self.random_hit()
        else:
            self.calc_scores()
            highscores = self.get_highscores()
            print(highscores)
            self.print_scores()
            slot = random.choice(highscores)
        return slot

    def print_scores(self):
        for row in self.slots_scores:
            print(row)

