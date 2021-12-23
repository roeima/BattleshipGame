import random
from typing import Dict

from battleship.bot import SmartBot, Bot
from battleship.constants import SHIPS_SIZES, FLEETS, FLEET_ONE, FLEET_TWO, HORIZONTAL_OPTIONS, VERTICAL_OPTIONS, \
    HORIZONTAL, VERTICAL, SHIP_SLOT, BOARD_SIZE
from battleship.player import Player
from battleship.ship import Ship

GAMEMODE_STR =\
"""
Which game mode do you want to play:
1. Single Player
2. MultiPlayer
"""

DIFFICULTY_STR =\
"""
Choose Difficulty:
1. EASY
2. HARD

enter difficulty (1/2) ---> """


def choose_fleet_prompt():
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
        return FLEETS[FLEET_ONE].copy()
    elif fleet_option == "2":
        return FLEETS[FLEET_TWO].copy()
    else:
        print("INVALID OPTION")
        return choose_fleet_prompt()


def place_ships_prompt(player: Player, fleet: Dict):
    for ship_name, amount in fleet.items():
        while amount > 0:
            player.print_board()
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

            if player.board.get_slot(row, column) == SHIP_SLOT:
                print("There is a ship in this slot")

            ship_slots = []
            if orientation is HORIZONTAL:
                ship_slots = [(row, column + x) for x in range(ship_size)]
            elif orientation is VERTICAL:
                ship_slots = [(row + x, column) for x in range(ship_size)]

            ship = Ship(ship_name, ship_size, ship_slots)
            if not player.board.check_ship_slots(ship):
                print(f"cannot place ship at ({row}, {column}) in {'HORIZONTAL' if orientation is HORIZONTAL else 'VERTICAL'}")
                continue

            player.add_ship(ship)
            amount -= 1


def check_inputs(row: str, column: str, orientation: str):
    inbounds = row.isdigit() and column.isdigit() and (0 <= int(row) < BOARD_SIZE) and (0 <= int(column) < BOARD_SIZE)
    valid_orientation = (orientation.upper() in HORIZONTAL_OPTIONS) or (orientation.upper() in VERTICAL_OPTIONS)
    return inbounds and valid_orientation


def hit_pormpt(player: Player):
    guesses = player.get_guess()
    print("Enter a row and column to hit")
    row = input("Row (0-9) ----> ")
    column = input("Column (0-9) ----> ")
    if not (row.isdigit() and column.isdigit() and (0 <= int(row) < BOARD_SIZE) and (0 <= int(column) < BOARD_SIZE)):
        print("Enter digits between 0-9")
        return hit_pormpt(guesses)
    elif (int(row), int(column)) in guesses:
        print(f"You have tried to hit {row}, {column}")
        return hit_pormpt(guesses)
    else:
        return int(row), int(column)


# TODO: delete only for testing
def random_slot():
    return random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)


# TODO: delete only for testing
def random_placement():
    row, column = random_slot()
    orientation = random.choice([HORIZONTAL, VERTICAL])
    return row, column, orientation


# TODO: delete only for testing
def place_ships_auto(player: Player, fleet):
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


# TODO: delete only for testing
def get_board_slots(player: Player):
    slots = []
    for ship in player.get_ships().copy():
        for slot in ship.get_slots().copy():
            slots.append(slot)
    return slots


# TODO: delete only for testing
def random_slot_from_slots(slots):
    slot = random.choice(slots)
    slots.remove(slot)
    return slot


def main():
    print("WELCOME TO BATTLESHIP GAME")
    print(GAMEMODE_STR)
    mode = input("choose game mode ---> ")
    if mode.upper() in ["S", "SINGLEPLAYER", "SINGEL PLAYER", "1"]:
        difficulty = input(DIFFICULTY_STR)

        if difficulty.upper() in ["2", "HARD", "H"]:
            bot = SmartBot()
        else:
            bot = Bot()

        player_fleet = choose_fleet_prompt()
        player: Player = Player()

        # TODO: remove auto ships place
        # place_ships_prompt(player, player_fleet)
        place_ships_auto(player, player_fleet)

        print()
        player.print_board()
        bot.place_ships()
        bot.print_board()

        current_player = "player"
        other_player = "bot"

        while True:
            if current_player == "player":
                # TODO: remove auto select row, col
                # row, col = hit_pormpt(player)
                row, col = 1, 1
                player.add_guess((row, col))
                if bot.hit_slot((row, col)):
                    print(f"you hit a ship in ({row}, {col})")

                    for ship in bot.get_ships().copy():
                        if not ship.is_alive():
                            print(f"You destroyed {ship.name}")
                            bot.remove_ship(ship)
                    if bot.lost():
                        print("YOU WON")
                        break
                else:
                    print("You missed")

            elif current_player == "bot":
                row, col = bot.guess()
                # row, col = random_slot_from_slots(player_ships_slots)
                if player.hit_slot((row, col)):
                    player.print_board()
                    print(f"bot hit a ship at ({row}, {col})")

                    if isinstance(bot, SmartBot):
                        bot.add_hit((row, col))

                    for ship in player.ships.copy():
                        if not ship.is_alive():
                            print(f"Bot destroyed your {ship.name}")
                            player.remove_ship(ship)
                    if player.lost():
                        print("Bot WON!!")
                        break
                else:
                    print(f"Bot tried to hit ({row}, {col}) and missed")
            current_player, other_player = other_player, current_player

    elif mode.upper() in ["M", "MULTIPLAYER", "MULTI PLAYER", "2"]:
        print("Multi")
    else:
        print(f"{mode} is Not A GAMEMODE")


if __name__ == '__main__':
    main()
