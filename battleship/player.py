from typing import Tuple, List

from battleship.board import Board
from battleship.constants import FLEETS, SHIPS_SIZES, FLEET_ONE, FLEET_TWO, HORIZONTAL_OPTIONS, BOARD_SIZE, HORIZONTAL,\
    SHIP_SLOT, VERTICAL
from battleship.ship import Ship
from battleship.utils import check_inputs


class Player:
    def __init__(self, name="Jonh Doe"):
        self.name = name
        self.board: Board = Board()
        self.hits = []
        self.ships: List[Ship] = []
        self.guesses: List[Tuple[int, int]] = []
        self.fleet = {}

    def lost(self):
        return len(self.ships) == 0

    def set_name(self, name):
        self.name = name

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

    def guess(self):
        return self.hit_pormpt()

    def place_ships(self):
        self.choose_fleet_prompt()
        self.place_ships_prompt()

    def choose_fleet_prompt(self):
        print("=====SHIPS=====")
        for ship, size in SHIPS_SIZES.items():
            print(f"SHIP: {ship} is {size} slots")
        print("=====FLEET OPTIONS=====")
        for option, fleet in FLEETS.items():
            print(f"* {option}")
            for ship, amount in fleet.items():
                print(f"   {ship}x{amount}")

        fleet_option = input("which fleet do you want to use (1/2) ---> ")

        if fleet_option == "1":
            self.fleet = FLEETS[FLEET_ONE].copy()
        elif fleet_option == "2":
            self.fleet = FLEETS[FLEET_TWO].copy()
        else:
            print("INVALID OPTION")
            return self.choose_fleet_prompt()

    def place_ships_prompt(self):
        for ship_name, amount in self.fleet.items():
            while amount > 0:
                self.print_board()
                print(f"Where do you want to place your {ship_name}")
                row_input = input("row (0-9) --> ")
                column_input = input("column (0-9) --> ")
                ship_size = SHIPS_SIZES[ship_name]
                orientation_input = input("Choose ship orientation (horizontal/vertical) --> ")

                if not check_inputs(row_input, column_input, orientation_input):
                    print(row_input, column_input, orientation_input)
                    print("Invalid inputs")
                    continue

                orientation = HORIZONTAL if orientation_input.upper() in HORIZONTAL_OPTIONS else VERTICAL
                row = int(row_input)
                column = int(column_input)

                if self.board.get_slot(row, column) == SHIP_SLOT:
                    print("There is a ship in this slot")

                ship_slots = []
                if orientation is HORIZONTAL:
                    ship_slots = [(row, column + x) for x in range(ship_size)]
                elif orientation is VERTICAL:
                    ship_slots = [(row + x, column) for x in range(ship_size)]

                ship = Ship(ship_name, ship_size, ship_slots)
                if not self.board.check_ship_slots(ship):
                    print(
                        f"cannot place ship at ({row}, {column}) in {'HORIZONTAL' if orientation is HORIZONTAL else 'VERTICAL'}")
                    continue

                self.add_ship(ship)
                amount -= 1

    def hit_pormpt(self):
        guesses = self.get_guess()
        print("Enter a row and column to hit")
        row = input("Row (0-9) ----> ")
        column = input("Column (0-9) ----> ")
        if not (row.isdigit() and column.isdigit() and (0 <= int(row) < BOARD_SIZE) and (
                0 <= int(column) < BOARD_SIZE)):
            print("Enter digits between 0-9")
            return self.hit_pormpt()
        elif (int(row), int(column)) in guesses:
            print(f"You have tried to hit {row}, {column}")
            return self.hit_pormpt()
        else:
            guess = (int(row), int(column))
            self.add_guess(guess)
            return guess
