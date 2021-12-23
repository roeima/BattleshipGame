from typing import Tuple, List


class Ship:
    def __init__(self, name, size, slots):
        self.name: str = name
        self.size: int = size
        self.slots: List[Tuple[int, int]] = slots

    def get_slots(self):
        return self.slots

    def hit_slot(self, slot: Tuple[int, int]):
        self.slots.remove(slot)

    def is_alive(self):
        return len(self.slots) > 0

    def __repr__(self):
        return f"Ship({self.name}, {self.size}, {self.slots})"
