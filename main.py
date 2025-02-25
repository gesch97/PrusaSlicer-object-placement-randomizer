import argparse
import logging
import os
from dataclasses import dataclass
from random import uniform
import random


@dataclass()
class PrintArea:
    X: float = -1.0
    Y: float = -1.0
    W: float = -1.0
    H: float = -1.0


def init_logging():
    file_location = os.path.dirname(__file__)
    file_name = "PrusaSlicer_loc_randomizer.log"
    log_file_path = os.path.join(file_location, file_name)
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Logging starts")


def get_gcode_argument(line: str, name_of_argument: str, get_position=False):
    pos = line.find(name_of_argument)
    end = line.find(" ", pos)
    if get_position:
        return pos + 1, end
    else:
        return float(line[pos + 1 : end])


def offset_axis(line, axis, offset):
    pos, end = get_gcode_argument(line, axis, get_position=True)
    line = line.replace(line[pos - 1 : end], f"{axis}{float(line[pos:end]) + offset}")
    return line


def offset_line(line, offset_x, offset_y):
    if "X" in line:
        line = offset_axis(line, "X", offset_x)
    if "Y" in line:
        line = offset_axis(line, "Y", offset_y)
    return line


def get_random_offset(printer_model, object_boundries):
    match printer_model:
        case "Prusa MK4S":
            printer_max_x = 250
            printer_max_y = 210
        case _:
            raise Exception("Unknow printer")

    MIN_GAP_FROM_EDGE = 2  # mm

    min_offset_x = -object_boundries.X + MIN_GAP_FROM_EDGE
    max_offset_x = printer_max_x - object_boundries.W
    min_offset_y = -object_boundries.Y + MIN_GAP_FROM_EDGE
    max_offset_y = printer_max_y - object_boundries.H
    logging.info(f"Offset range X: {min_offset_x} - {max_offset_x}")
    logging.info(f"Offset range Y: {min_offset_y} - {max_offset_y}")

    offset_x = random.uniform(min_offset_x, max_offset_x)
    offset_y = random.uniform(min_offset_y, max_offset_y)

    logging.info(f"Random offset (x,y): ({offset_x}, {offset_y})")
    return offset_x, offset_y


def get_offset(x_ofs, y_ofs):
    if x_ofs > 1 or y_ofs > 1:
        raise Exception("Offset coefficient can't be larger than 1")
    if x_ofs < 0 or y_ofs < 0:
        raise Exception("Offset coefficient can't be smaller than 0")


def check_if_pt_in_printarea(print_area: PrintArea, line: str):
    if "X" in line:
        xcoord = get_gcode_argument(line, "X", get_position=False)
        if xcoord < print_area.X:
            return False
        if xcoord > print_area.X + print_area.W:
            return False
    if "Y" in line:
        xcoord = get_gcode_argument(line, "Y", get_position=False)
        if xcoord < print_area.Y:
            return False
        if xcoord > print_area.Y + print_area.H:
            return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="A python script to be used as a PrusaSlicer post processing step. It moves all objects to a random place instead of the default middle of the print bed."
    )
    parser.add_argument("Path", help="Path for the gcode to be edited", type=str)
    parser.add_argument(
        "printer_model",
        help="The model of your 3D printed.",
        choices=[
            "Prusa MK4S",
        ],
        type=str,
    )
    args = parser.parse_args()
    path = vars(args)["Path"]
    printer_model = vars(args)["printer_model"]
    logging.info(f"The following path was provided: {path}")

    with open(path) as f:
        lines = f.read().split("\n")

    mfff_line = next(filter(lambda line: line.startswith("M555"), lines))
    bed_area = PrintArea()
    for word in mfff_line.split(" "):
        match word[0]:
            case "X":
                bed_area.X = int(word[1:])
            case "Y":
                bed_area.Y = int(word[1:])
            case "W":
                bed_area.W = int(word[1:])
            case "H":
                bed_area.H = int(word[1:])

    logging.info(f"old print area: {bed_area}")

    offset_x, offset_y = get_random_offset(printer_model, bed_area)

    for i, line in enumerate(lines):
        # print(line)
        words = line.split(" ")
        match words[0]:
            case "M555":
                lines[i] = offset_line(line, offset_x, offset_y)
            case "G0" | "G1" | "G2" | "G3":
                if not check_if_pt_in_printarea(bed_area, line):
                    continue
                if "X" in line or "Y" in line:
                    lines[i] = offset_line(line, offset_x, offset_y)

    output_as_string = "\n".join(lines)
    with open("output.gcode", "w") as text_file:
        text_file.write(output_as_string)


if __name__ == "__main__":
    init_logging()
    main()
