from battleship.bot import SmartBot, Bot
from battleship.constants import EASY, HARD, SINGLE_PLAYER, MULTI_PLAYER, GAMEMODE_STR, DIFFICULTY_STR, PLAYER, OTHER
from battleship.player import Player


class BattleShipGame:
    def __init__(self):
        self.is_running = True
        self.difficulty = EASY
        self.gamemode = SINGLE_PLAYER
        self.other_player = None
        self.player = Player()
        self.current_player = "player"

    def run(self):
        print("WELCOME TO BATTLESHIP GAME")
        name = input("What is your name? --> ")
        self.player.set_name(name)
        self.choose_gamemode()
        if self.gamemode == SINGLE_PLAYER:
            self.choose_difficulty()

            if self.difficulty == HARD:
                self.other_player = SmartBot()
            else:
                self.other_player = Bot()

        self.player.place_ships()
        self.player.print_board()

        if self.gamemode == SINGLE_PLAYER:
            self.other_player.place_ships()
            self._run_singleplayer()
        else:
            self._run_multiplayer()

        play_again = input("YOU WISH TO PLAY AGAIN (y/n) ---> ")
        if play_again.upper() in ["YES", "Y"]:
            self.run()

    def _run_singleplayer(self):
        while self.is_running:
            if self.current_player == PLAYER:

                row, col = self.player.guess()
                self.player.add_guess((row, col))
                if self.other_player.hit_slot((row, col)):
                    print(f"you hit a ship in ({row}, {col})")

                    for ship in self.other_player.get_ships().copy():
                        if not ship.is_alive():
                            print(f"You destroyed {ship.name}")
                            self.other_player.remove_ship(ship)
                        if self.other_player.lost():
                            print("YOU WON")
                            break
                else:
                    print("YOU MISSED")

                self.current_player = OTHER

            elif self.current_player == OTHER:
                row, col = self.other_player.guess()

                if self.player.hit_slot((row, col)):
                    self.player.print_board()
                    print(f"{self.other_player.name} hit a ship at ({row}, {col})")

                    if isinstance(self.other_player, SmartBot):
                        self.other_player.add_hit((row, col))

                    for ship in self.player.get_ships().copy():
                        if not ship.is_alive():
                            print(f"{self.other_player.name} destroyed your {ship.name}")
                            self.player.remove_ship(ship)

                    if self.player.lost():
                        print(f"{self.other_player.name} WON!!")
                        break
                else:
                    print(f"{self.other_player.name} tried to hit ({row}, {col}) and missed")

                self.current_player = PLAYER

    def _run_multiplayer(self):
        pass

    def choose_gamemode(self):
        mode = input(GAMEMODE_STR)
        if mode.upper() in ["1", "SINGLE", "SINGLEPLAYER", "SINGLE PLAYER"]:
            self.gamemode = SINGLE_PLAYER
        elif mode.upper() in ["2", "MULTI", "MULTIPLAYER", "MULTIPLAYER"]:
            self.gamemode = MULTI_PLAYER
        else:
            print(f"`{mode}` `is not a valid gamemode choose again")
            self.choose_gamemode()

    def choose_difficulty(self):
        diff = input(DIFFICULTY_STR)
        if diff in ["2", "HARD", "H"]:
            self.difficulty = HARD
        elif diff in ["1", "EASY", "E"]:
            self.difficulty = EASY
        else:
            print(f"`{diff}` is not a valid difficulty choose again")
            self.choose_difficulty()

