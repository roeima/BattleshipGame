import json
import socket
from typing import Tuple, List
import threading


class NetPlayer:
    def __init__(self, address, connection: socket.socket):
        self.conn = connection
        self.addr = address
        self.name = ""

    def set_name(self):
        self.name = self.get_name()

    def get_name(self):
        action = json.dumps(
            {
                "action": "get_name"
            }
        )
        return self.send_action(action)

    def guess(self):
        action = json.dumps(
            {
                "action": "guess"
            }
        )
        return self.send_action(action)

    def hit_slot(self, slot: Tuple[int, int]):
        action = json.dumps(
            {
                "action": "hit_slot",
                "row": slot[0],
                "col": slot[1]
            }
        )
        return self.send_action(action)

    def lost(self):
        action = json.dumps(
            {
                "action": "lost"
            }
        )
        return self.send_action(action)

    def end_game(self):
        action = json.dumps(
            {
                "action": "end_game"
            }
        )
        return self.send_action(action)

    def send_result(self, msg):
        message = json.dumps(
            {
                "msg": msg
            }
        )
        self.conn.send(message.encode())
        return json.loads(self.conn.recv(2048).decode())

    def send_action(self, action):
        self.conn.send(action.encode())
        result = json.loads(self.conn.recv(2048).decode())
        return self.parse_result(result)

    def parse_result(self, result):
        if 'action' in result:
            if result['action'] == 'guess':
                return int(result['row']), int(result['col'])

            if result['action'] == 'hit_slot':
                return result['hit'], (result['ship_removed'], result['ship_name'])

            if result['action'] == 'lost':
                return result['lost']

            if result['action'] == 'get_name':
                return result['name']

            if result['action'] == 'end_game':
                return result['msg']


def start_game(players: List[NetPlayer]):
    print("started")
    running = True
    current_player = 0
    other_player = 1

    for player in players:
        player.set_name()

    while running:
        player = players[current_player]
        other = players[other_player]

        row, col = player.guess()

        hit, ship_down = players[other_player].hit_slot((row, col))

        if hit:
            player.send_result(f"{player.name} [{player.addr}] tried to hit ({row}, {col}) and hit a ship")
            other.send_result(f"{player.name} [{player.addr}] tried to hit ({row}, {col}) and hit a ship")

            if ship_down[0]:
                player.send_result(f"{player.name} [{player.addr}] destroyed {ship_down[1]}")
                other.send_result(f"{player.name} [{player.addr}] destroyed {ship_down[1]}")
        else:
            player.send_result(f"{player.name} [{player.addr}] tried to hit ({row},{col}) and missed")
            other.send_result(f"{player.name} [{player.addr}] tried to hit ({row},{col}) and missed")

        if player.lost():
            player.send_result(f"{other.name} [{other.addr}] WON!!")
            other.send_result(f"{other.name} [{other.addr}] WON!!")
            player.end_game()
            other.end_game()
            running = False

        current_player, other_player = other_player, current_player


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ''
        self.port = 5555
        self.players = []

    def run(self):
        try:
            self.sock.bind((self.ip, self.port))

        except socket.error as e:
            print(e)

        self.sock.listen(2)
        print("Waiting for players to join the server.....")

        while True:
            conn, addr = self.sock.accept()
            print(f'Connection from: {addr}')
            self.players.append(NetPlayer(addr, conn))

            if len(self.players) == 2:
                threading.Thread(target=start_game, args=(self.players.copy(), )).start()
                self.players = []


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
