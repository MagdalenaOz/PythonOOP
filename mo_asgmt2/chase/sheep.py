import random
import logging


class Sheep:
    def __init__(self, seq_number, move_range=0.5, init_pos_limit=10.0):
        self.seq_number = seq_number
        self.pos_x = random.uniform(-init_pos_limit, init_pos_limit)
        self.pos_y = random.uniform(-init_pos_limit, init_pos_limit)
        self.move_range = move_range
        logging.debug(f"Sheep number {self.seq_number} initialized on "
                      f"position ({self.pos_x:.3f}, {self.pos_y:.3f}).")

    def move(self):
        direction = random.choice(["n", "s", "e", "w"])
        logging.debug(f"Sheep number {self.seq_number} chose direction '{direction}'.")
        if direction == "e":
            self.pos_x += self.move_range
        elif direction == "n":
            self.pos_y += self.move_range
        elif direction == "w":
            self.pos_x -= self.move_range
        elif direction == "s":
            self.pos_y -= self.move_range

        logging.debug(f"Sheep number {self.seq_number} moved to "
                      f"position ({self.pos_x:.3f}, {self.pos_y:.3f}).")
