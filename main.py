import argparse


def main():
    print("Hi, this a PrusaSlicer post-process script!")
    parser = argparse.ArgumentParser(
        description="A python script to be used as a PrusaSlicer post processing step. It moves all objects to a random place instead of the default middle of the print bed."
    )
    parser.add_argument("Path", help="Path for the gcode to be edited", type=str)
    args = parser.parse_args()
    path = vars(args)["Path"]
    print(path)


if __name__ == "__main__":
    main()
