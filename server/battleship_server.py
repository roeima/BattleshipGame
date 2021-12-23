from enum import Enum, auto


class CODES(Enum):
    JOIN = auto()
    CREATE = auto()
    HIT = auto()


class Server:
    def __init__(self):
        pass

    def run(self):
        pass

    def handle_code(self, code):
        pass
