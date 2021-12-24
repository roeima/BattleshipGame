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


def check_inputs(row: str, column: str, orientation: str):
    inbounds = row.isdigit() and column.isdigit() and (0 <= int(row) < BOARD_SIZE) and (0 <= int(column) < BOARD_SIZE)
    valid_orientation = (orientation.upper() in HORIZONTAL_OPTIONS) or (orientation.upper() in VERTICAL_OPTIONS)
    return inbounds and valid_orientation
