import unittest
from main import PrintArea, check_if_pt_in_printarea, get_gcode_argument, offset_line


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.line1 = "G1 X0 Y0 W50 H54"
        self.line2 = "G1 X100 Y0 W50 H54"
        self.line3 = "M555 X100 Y76 W50 H54"
        self.line4 = "G0 X100 Y100 E4 F500 ; purge"
        self.line5 = "G0 X100 Y150 E4 F500 ; purge"

    def test_offset_line(self):
        self.assertEqual(offset_line(self.line1, 10, 20), "G1 X10.0 Y20.0 W50 H54")
        self.assertEqual(offset_line(self.line2, -10, 20), "G1 X90.0 Y20.0 W50 H54")
        self.assertEqual(offset_line(self.line3, 10, 20), "M555 X110.0 Y96.0 W50 H54")

    def test_get_gcode_argument(self):
        self.assertEqual(get_gcode_argument("G0 X25 E4 F500 ; purge", "X"), 25)
        self.assertEqual(
            get_gcode_argument("G0 X25 E4 F500 ; purge", "X", get_position=True), (4, 6)
        )

    def test_check_if_pt_in_printarea(self):
        pa = PrintArea(90, 90, 20, 20)
        pa2 = PrintArea(100, 90, 20, 20)
        pa3 = PrintArea(90, 100, 20, 20)
        self.assertEqual(check_if_pt_in_printarea(pa, self.line1), False)
        self.assertEqual(check_if_pt_in_printarea(pa2, self.line4), True)
        self.assertEqual(check_if_pt_in_printarea(pa3, self.line4), True)

        self.assertEqual(check_if_pt_in_printarea(pa2, self.line5), False)
        self.assertEqual(check_if_pt_in_printarea(pa3, self.line5), False)
