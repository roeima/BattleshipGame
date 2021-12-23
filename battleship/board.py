from typing import List
from battleship.constants import WATER_SLOT, SHIP_SLOT, HIT_SLOT, BOARD_SIZE
from battleship.ship import Ship


class Board:
    def __init__(self):
        self._board: List[List[int]] = [[WATER_SLOT]*BOARD_SIZE for _ in range(BOARD_SIZE)]

    def print_board(self):
        numbers_row = "----0---1---2---3---4---5---6---7---8---9--"
        row_format = "{idx} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |"
        row_delimiter = "-------------------------------------------"
        print(numbers_row)
        for idx, row in enumerate(self._board):
            print(row_format.format(idx=idx, *row))
            print(row_delimiter)

    def get_slot(self, row, col):
        return self._board[row][col]

    def check_ship_slots(self, ship: Ship):
        ship_slots = ship.get_slots()
        for row, col in ship_slots:
            if not self.check_slot(row, col):
                return False
        return True

    def check_slot(self, row: int, column: int):
        # check if row, column are in bounds
        if (row < 0 or row >= len(self._board)) or (column < 0 or column >= len(self._board[0])):
            return False
        # chek if row, column is a ship slot
        if self._board[row][column] == SHIP_SLOT:
            return False
        # check if neighbors equal to 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif 0 <= row + i < len(self._board) and 0 <= column + j < len(self._board):
                    if self._board[row + i][column + j] == SHIP_SLOT:
                        return False
        return True

    def place_ship(self, ship: Ship):
        ship_slots = ship.get_slots()
        for row, col in ship_slots:
            self._board[row][col] = SHIP_SLOT

    def hit_slot(self, row: int, col: int):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self._board[row][col] == SHIP_SLOT:
                self._board[row][col] = HIT_SLOT
                return True
            elif self._board[row][col] == HIT_SLOT or self._board[row][col] == WATER_SLOT:
                return False
        else:
            return False
