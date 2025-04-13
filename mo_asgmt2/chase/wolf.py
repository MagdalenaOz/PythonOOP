import math
import logging


class Wolf:

    def __init__(self, move_range=1.0):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.move_range = move_range

    def calculate_distance(self, sheep_pos_x, sheep_pos_y):
        distance = math.sqrt((sheep_pos_x - self.pos_x) * (sheep_pos_x - self.pos_x) +
                             (sheep_pos_y - self.pos_y) * (sheep_pos_y - self.pos_y))
        return distance

    def find_nearest_sheep(self, sheep_list):
        nearest_sheep = None
        shortest_distance = float('inf')

        for sheep in sheep_list:
            if sheep is not None:
                distance = self.calculate_distance(sheep.pos_x, sheep.pos_y)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_sheep = sheep

        logging.debug(f"Wolf determined the shortest distance is to "
                      f"sheep number {nearest_sheep.seq_number} "
                      f"with value: {shortest_distance:.3f}.")

        return nearest_sheep, shortest_distance

    def chase_sheep(self, sheep_list):
        nearest_sheep, distance = self.find_nearest_sheep(sheep_list)
        is_chased = False
        is_eaten = False
        seq_num = None

        if nearest_sheep is not None:
            seq_num = nearest_sheep.seq_number
            if distance <= self.move_range:
                self.eat_sheep(nearest_sheep, sheep_list)
                is_eaten = True
                logging.info(f"The wolf has eaten sheep number {nearest_sheep.seq_number}.")
            else:
                self.move_towards_sheep(nearest_sheep)
                is_chased = True
                logging.info(f"The wolf is chasing sheep number {nearest_sheep.seq_number}.")

        logging.debug(f"The wolf moved to "
                      f"position ({self.pos_x:.3f}, {self.pos_y:.3f}).")
        logging.info("The wolf moved.")

        return seq_num, is_eaten, is_chased

    def eat_sheep(self, sheep, sheep_list):
        self.pos_x = sheep.pos_x
        self.pos_y = sheep.pos_y

        sheep_list[sheep.seq_number - 1] = None

    def move_towards_sheep(self, sheep):
        delta_x = sheep.pos_x - self.pos_x
        delta_y = sheep.pos_y - self.pos_y

        distance = self.calculate_distance(sheep.pos_x, sheep.pos_y)

        self.pos_x += (delta_x / distance) * self.move_range
        self.pos_y += (delta_y / distance) * self.move_range
