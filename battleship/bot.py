import random
from typing import Tuple

from battleship.constants import HORIZONTAL, VERTICAL, SHIPS_SIZES, FLEET_ONE, FLEET_TWO, FLEETS, BOARD_SIZE
from battleship.player import Player
from battleship.ship import Ship
from battleship.utils import random_placement


class Bot(Player):
    def __init__(self):
        super(Bot, self).__init__("BOT")
        self.init_guesses()

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
                    self.add_ship(ship)
                    amount -= 1

    def random_hit(self):
        slot = random.choice(self.guesses)
        self.guesses.remove(slot)
        return slot

    def init_guesses(self):
        self.guesses = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.guesses.append((row, col))

    def guess(self):
        return self.random_hit()


class SmartBot(Bot):
    def __init__(self):
        super(SmartBot, self).__init__()
        self.slots_scores = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]

    def add_hit(self, hit: Tuple[int, int]):
        self.hits.append(hit)

    def calc_scores(self):
        for row, col in self.hits:
            self.slots_scores[row][col] = -1

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.slots_scores[row][col] == -1 or self.slots_scores[row][col] == -2:
                    continue

                if self.check_across(row, col):
                    self.slots_scores[row][col] = 5

                if self.check_diagonal(row, col):
                    self.slots_scores[row][col] = -2

                if (not (row, col) in self.guesses) and self.slots_scores[row][col] == 5:
                    self.slots_scores[row][col] = -2

    def check_diagonal(self, row, col):
        return (0 <= row - 1 < BOARD_SIZE and 0 <= col - 1 < BOARD_SIZE and self.slots_scores[row - 1][col - 1] == -1) or \
                (0 <= row - 1 < BOARD_SIZE and 0 <= col + 1 < BOARD_SIZE and self.slots_scores[row - 1][col + 1] == -1) or \
                (0 <= row + 1 < BOARD_SIZE and 0 <= col - 1 < BOARD_SIZE and self.slots_scores[row + 1][col - 1] == -1) or \
                (0 <= row + 1 < BOARD_SIZE and 0 <= col + 1 < BOARD_SIZE and self.slots_scores[row + 1][col + 1] == -1)

    def check_across(self, row, col):
        return (0 <= row - 1 < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.slots_scores[row - 1][col] == -1) or \
               (0 <= row < BOARD_SIZE and 0 <= col + 1 < BOARD_SIZE and self.slots_scores[row][col + 1] == -1) or \
               (0 <= row + 1 < BOARD_SIZE and 0 <= col + 1 < BOARD_SIZE and self.slots_scores[row + 1][col] == -1) or \
               (0 <= row < BOARD_SIZE and 0 <= col - 1 < BOARD_SIZE and self.slots_scores[row][col - 1] == -1)

    def get_highscores(self):
        highscores = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.slots_scores[row][col] == 5:
                    highscores.append((row, col))
        return highscores

    def guess(self):
        if self.hits:
            self.calc_scores()
            self.print_scores()
            highscores = self.get_highscores()
            if highscores:
                slot = random.choice(highscores)
                self.guesses.remove(slot)
            else:
                slot = self.random_hit()
        else:
            slot = self.random_hit()

        return slot

    def print_scores(self):
        for row in self.slots_scores:
            print(row)

