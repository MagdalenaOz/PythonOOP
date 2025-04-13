import json
import csv
import logging

from wolf import Wolf
from sheep import Sheep


class Simulation:
    def __init__(self, max_rounds=50, sheep_quantity=15, init_pos_limit=10.0, sheep_move_range=0.5,
                 wolf_move_range=1.0):
        self.max_rounds = max_rounds
        self.sheep_quantity = sheep_quantity
        self.init_pos_limit = init_pos_limit
        self.sheep_move_range = sheep_move_range
        self.wolf_move_range = wolf_move_range
        self.sheep_list = [Sheep(i + 1, sheep_move_range, init_pos_limit) for i in range(sheep_quantity)]
        logging.info("Initial position of all sheep determined.")
        self.wolf = Wolf(wolf_move_range)
        self.round_num = 0
        self.positions_data = []
        self.alive_sheep_data = []

    def simulate_rounds(self, wait=False):
        self.display_start_info()

        while self.round_num < self.max_rounds and self.count_alive_sheep() > 0:
            self.round_num += 1
            logging.info(f"Started round {self.round_num}.")

            for sheep in self.sheep_list:
                if sheep is not None:
                    sheep.move()
            logging.info("All alive sheep moved.")

            seq_num, is_eaten, is_chased = self.wolf.chase_sheep(self.sheep_list)

            self.display_status_info(is_eaten, is_chased, seq_num)

            self.save_alive_sheep_to_csv_file()
            self.save_positions_to_json_file()

            logging.info(f"Round {self.round_num} ended "
                         f"with {self.count_alive_sheep()} alive sheep.")

            if wait:
                input("Press 'enter' to continue...")

            if self.round_num == self.max_rounds:
                logging.info(
                    "Simulation terminated, because maximum number of rounds has been reached.")
            if self.count_alive_sheep() == 0:
                logging.info("Simulation terminated, because all sheep have been eaten.")

    def save_positions_to_json_file(self, positions_file_path="pos.json"):
        data = {
            "round_no": self.round_num,
            "wolf_pos": [self.wolf.pos_x, self.wolf.pos_y],
            "sheep_pos": [(sheep.pos_x, sheep.pos_y) if sheep is not None else None
                          for sheep in self.sheep_list],
        }

        self.positions_data.append(data)

        try:
            with open(positions_file_path, 'w') as json_file:
                json.dump(self.positions_data, json_file, indent=2)
            logging.debug(f"Information about positions saved to {positions_file_path} file.")
        except IOError as e:
            logging.error(f"Failed saving info about positions to {positions_file_path} file: {e}")

    def save_alive_sheep_to_csv_file(self, alive_file_path="alive.csv"):
        alive_sheep_count = self.count_alive_sheep()

        self.alive_sheep_data.append([self.round_num, alive_sheep_count])

        try:
            with open(alive_file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Round_no', 'Alive_sheep'])
                writer.writerows(self.alive_sheep_data)
            logging.debug(f"Information about alive sheep saved to {alive_file_path} file.")
        except IOError as e:
            logging.error(f"Failed saving info about alive sheep to {alive_file_path} file: {e}")

    def count_alive_sheep(self):
        return sum(1 for sheep in self.sheep_list if sheep is not None)

    def display_start_info(self):
        print("Start info")
        print(f"Wolf initial position: ({self.wolf.pos_x:.3f}, {self.wolf.pos_y:.3f})")
        print(f"Rounds: {self.max_rounds}")
        print(f"Sheep number: {self.sheep_quantity}")

    def display_status_info(self, is_eaten, is_chased, seq_num):
        print(f"--- Round {self.round_num} ---")
        print(f"    Wolf position: ({self.wolf.pos_x:.3f}, {self.wolf.pos_y:.3f})")
        print(f"    Alive sheep count: {self.count_alive_sheep()}")

        if is_eaten:
            print(f"    Wolf has eaten sheep number {seq_num}")
        elif is_chased:
            print(f"    Wolf is chasing sheep number {seq_num}")
