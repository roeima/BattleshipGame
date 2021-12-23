import json
import socket

from battleship.bot import SmartBot, Bot
from battleship.constants import EASY, HARD, SINGLE_PLAYER, MULTI_PLAYER, GAMEMODE_STR, DIFFICULTY_STR, SERVER_HOST, \
    SERVER_PORT
from battleship.player import Player


class BattleShipGame:
    def __init__(self):
        self._init_game()

    def _init_game(self):
        self.is_running = True
        self.difficulty = EASY
        self.gamemode = SINGLE_PLAYER
        self.player = Player()
        self.current_player = self.player
        self.other_player = None

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
            self._init_game()
            self.run()

    def _run_singleplayer(self):
        while self.is_running:

            row, col = self.current_player.guess()

            if self.other_player.hit_slot((row, col)):

                if self.current_player != self.player:
                    self.player.print_board()

                print(f"{self.current_player.name} hit a ship at ({row}, {col})")

                if isinstance(self.current_player, SmartBot):
                    self.current_player.add_hit((row, col))

                for ship in self.other_player.get_ships().copy():
                    if not ship.is_alive():
                        print(f"{self.current_player.name} destroyed {self.other_player.name} {ship.name}")
                        self.other_player.remove_ship(ship)

                if self.other_player.lost():
                    print(f"{self.current_player.name} WON!!")
                    break
            else:
                print(f"{self.current_player.name} tried to hit ({row}, {col}) and missed")

            if self.current_player == self.player:
                self.current_player = self.other_player
                self.other_player = self.player

            else:
                self.other_player = self.current_player
                self.current_player = self.player

    def _run_multiplayer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((SERVER_HOST, SERVER_PORT))
            except ConnectionRefusedError as e:
                print("Server is DOWN")
                return
            while self.is_running:
                try:
                    data = s.recv(2048)
                    s.send(self.parse_message(data))
                except Exception as e:
                    print("Error while connecting to server")
                    return

    def parse_message(self, message_to_parse):
        message = json.loads(message_to_parse.decode())
        return_msg = {}
        if 'action' in message:

            if message['action'] == 'end_game':
                self.is_running = False
                return_msg = {
                    "action": "end_game",
                    "msg": "bye!!"
                }

            if message['action'] == 'get_name':
                name = self.player.name
                return_msg = {
                    "action": "get_name",
                    "name": name
                }

            if message['action'] == 'guess':
                row, col = self.player.guess()
                return_msg = {
                    "action": "guess",
                    "row": row,
                    "col": col,
                    "result": True
                }

            if message['action'] == 'lost':
                lost = self.player.lost()
                return_msg = {
                    "action": "lost",
                    "lost": lost,
                    "result": True
                }

            if message['action'] == 'hit_slot':
                row, col = int(message['row']), int(message['col'])
                hit = self.player.hit_slot((row, col))
                ship_removed = False
                ship_name = ""
                for ship in self.player.get_ships().copy():
                    if not ship.is_alive():
                        ship_removed = True
                        ship_name = ship.name
                        self.player.remove_ship(ship)

                self.player.print_board()

                return_msg = {
                    "action": "hit_slot",
                    "hit": hit,
                    "ship_removed": ship_removed,
                    "ship_name": ship_name,
                    "result": True
                }

        elif 'msg' in message:
            print(message['msg'])

        return json.dumps(return_msg).encode()

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

