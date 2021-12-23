import random

from battleship.constants import BOARD_SIZE, HORIZONTAL, VERTICAL, SHIPS_SIZES, HORIZONTAL_OPTIONS, VERTICAL_OPTIONS, \
    FLEET_TWO, FLEETS, FLEET_ONE
from battleship.ship import Ship


def random_slot():
    return random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)


def random_placement():
    row, column = random_slot()
    orientation = random.choice([HORIZONTAL, VERTICAL])
    return row, column, orientation


def place_ships_auto(player):
    fleet = random.choice([FLEETS[FLEET_ONE].copy(), FLEETS[FLEET_TWO].copy()])
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
            if player.board.check_ship_slots(ship):
                player.add_ship(ship)
                amount -= 1


def check_inputs(row: str, column: str, orientation: str):
    inbounds = row.isdigit() and column.isdigit() and (0 <= int(row) < BOARD_SIZE) and (0 <= int(column) < BOARD_SIZE)
    valid_orientation = (orientation.upper() in HORIZONTAL_OPTIONS) or (orientation.upper() in VERTICAL_OPTIONS)
    return inbounds and valid_orientation
