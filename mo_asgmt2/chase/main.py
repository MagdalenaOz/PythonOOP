import argparse
import configparser
import logging
import os
import sys

from simulation import Simulation


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulation of a wolf chasing sheep.")
    parser.add_argument("-c", "--config", type=str, metavar="FILE",
                        help="Path to configuration file, where FILE stands for a filename.")
    parser.add_argument("-l", "--log", type=str, metavar="LEVEL",
                        help="Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).")
    parser.add_argument("-r", "--rounds", type=int, metavar="NUM", default=50,
                        help="Maximum number of rounds, where NUM denotes an integer.")
    parser.add_argument("-s", "--sheep", type=int, metavar="NUM", default=15,
                        help="Number of sheep, where NUM denotes an integer.")
    parser.add_argument("-w", "--wait", action="store_true",
                        help="Wait for key press at the end of each round.")
    return parser.parse_args()


def load_config(config_file_path):
    if not os.path.isfile(config_file_path):
        logging.error(f"File '{config_file_path}' not found.")
        raise FileNotFoundError(f"File '{config_file_path}' does not exist.")

    config = configparser.ConfigParser()
    config.read(config_file_path)
    try:
        init_pos_limit = float(config.get('Sheep', 'InitPosLimit'))
        sheep_move_range = float(config.get('Sheep', 'MoveDist'))
        wolf_move_range = float(config.get('Wolf', 'MoveDist'))

        logging.debug(f"Configuration loaded from {config_file_path}: "
                      f"init_pos_limit={init_pos_limit}, "
                      f"sheep_move_range={sheep_move_range}, "
                      f"wolf_move_range={wolf_move_range}.")

        if init_pos_limit <= 0 or sheep_move_range <= 0 or wolf_move_range <= 0:
            logging.error(f"Config values are not greater than zero. Given: InitPosLimit={init_pos_limit}, "
                          f"MoveDist (sheep)={sheep_move_range}, MoveDist (wolf)={wolf_move_range}.")
            raise ValueError("Config values must be greater than zero.")

        return init_pos_limit, sheep_move_range, wolf_move_range

    except configparser.NoOptionError as e:
        logging.error(f"Missing configuration option: {e}.")
        raise ValueError(f"Missing configuration option: {e}")

    except ValueError as e:
        logging.error(f"Invalid configuration value: {e}.")
        raise ValueError(f"Invalid configuration value: {e}")


def configure_logging(log_level):
    if log_level is None:
        raise ValueError(f"Invalid log level.")
    else:
        logging.basicConfig(
            filename='chase.log',
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='w'
        )


def main():
    args = parse_arguments()

    try:
        if args.rounds <= 0:
            raise ValueError("Max rounds must be greater than zero!")
        if args.sheep <= 0:
            raise ValueError(f"Number of sheep must be greater than zero!")
    except ValueError as e:
        print(f"Argument error: {e}")
        sys.exit(1)

    if args.log:
        log_level = getattr(logging, args.log.upper(), None)
        configure_logging(log_level)

    if args.config:
        init_pos_limit, sheep_move_range, wolf_move_range = load_config(args.config)
    else:
        init_pos_limit, sheep_move_range, wolf_move_range = 10.0, 0.5, 1.0

    simulation = Simulation(
        max_rounds=args.rounds,
        sheep_quantity=args.sheep,
        init_pos_limit=init_pos_limit,
        sheep_move_range=sheep_move_range,
        wolf_move_range=wolf_move_range,
    )
    simulation.simulate_rounds(args.wait)


if __name__ == "__main__":
    main()
