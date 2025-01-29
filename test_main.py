import unittest
from main import offset_line


class Tests(unittest.TestCase):
    def test_offset_line(self):
        self.assertEqual(
            offset_line("M555 X100 Y76 W50 H54", 10, 20), "M555 X110 Y96 W50 H54"
        )
        self.assertEqual(offset_line("G1 X0 Y0 W50 H54", 10, 20), "G1 X10 Y20 W50 H54")
        self.assertEqual(
            offset_line("G1 X100 Y0 W50 H54", -10, 20), "G1 X90 Y20 W50 H54"
        )
