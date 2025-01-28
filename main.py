import argparse
import logging


def init_logging():
    logging.basicConfig(filename="loc_randomizer.log", level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Logging starts")


def main():
    print("Hi, this a PrusaSlicer post-process script!")
    parser = argparse.ArgumentParser(
        description="A python script to be used as a PrusaSlicer post processing step. It moves all objects to a random place instead of the default middle of the print bed."
    )
    parser.add_argument("Path", help="Path for the gcode to be edited", type=str)
    args = parser.parse_args()
    path = vars(args)["Path"]
    logging.info(f"The following path was provided: {path}")


if __name__ == "__main__":
    init_logging()
    main()
