from typing import Tuple, List

CARRIER = "Carrier"
BATTLESHIP = "Battleship"
CRUISER = "Cruiser"
DESTROYER = "Destroyer"
SUBMARINE = "Submarine"

SHIPS = (CARRIER, BATTLESHIP, CRUISER, DESTROYER, SUBMARINE)

SHIPS_SIZES = {
    CARRIER: 5,
    BATTLESHIP: 4,
    CRUISER: 3,
    DESTROYER: 2,
    SUBMARINE: 1
}

FLEET_ONE = "FLEET ONE"
FLEET_TWO = "FLEET TWO"

HORIZONTAL_OPTIONS = ["HORIZONTAL", "H"]
VERTICAL_OPTIONS = ["VERTICAL", "V"]
HORIZONTAL = "H"
VERTICAL = "V"

FLEETS = {
    FLEET_ONE: {
        CARRIER: 1,
        BATTLESHIP: 1,
        CRUISER: 2,
        DESTROYER: 1,
        SUBMARINE: 0
    },
    FLEET_TWO: {
        CARRIER: 0,
        BATTLESHIP: 1,
        CRUISER: 2,
        DESTROYER: 3,
        SUBMARINE: 4
    }
}

SHIP_SLOT = "0"
WATER_SLOT = " "
HIT_SLOT = "X"

Board = List[List[str]]
Slot = Tuple[int, int]