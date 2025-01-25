from context import table_of_offsets

import unittest
import os

source_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Test_TableOfOffsets(unittest.TestCase):

    def test_1(self):
        print(table_of_offsets.__version__)
        actual = table_of_offsets.TableOfOffsets()
        self.assertIsNotNone(actual)
        self.assertTrue(actual.verify_triplet("1-2-3"))

    def test_offset2double(self):
        self.assertEqual(1.0, table_of_offsets.TableOfOffsets.offset2double("0-1-0"))
        self.assertEqual(1.0, table_of_offsets.TableOfOffsets.offset2double("0-1"))
        self.assertEqual(12.0, table_of_offsets.TableOfOffsets.offset2double("1-0"))

        self.assertEqual(
            0.1875, table_of_offsets.TableOfOffsets.offset2double("0-0-1+")
        )
        self.assertEqual(
            0.0625, table_of_offsets.TableOfOffsets.offset2double("0-0-1-")
        )

        with self.assertRaises(Exception):
            table_of_offsets.TableOfOffsets.offset2double("0-0-1--")
        with self.assertRaises(Exception):
            table_of_offsets.TableOfOffsets.offset2double("")
        with self.assertRaises(Exception):
            table_of_offsets.TableOfOffsets.offset2double("a-b-c")

    def test_Model(self):
        actual = table_of_offsets.Model(
            os.path.join(source_directory, "sample_data/offset_table.csv")
        )
        self.assertIsNotNone(actual._too)

        stations = actual.station_positions()
        self.assertIs(type(stations), dict)
        self.assertEqual(18, len(stations))

        actual_sheer = actual.loft_sheer()
        # print(sheer)
        """
        [
            (12, 22.25), (36, 20.75), (60, 19.875), (84, 19.25), 
            (108, 19.0), (132, 18.875), (156, 19.125), (180, 19.75), 
            (204, 20.625), (228, 21.625), (252, 23.0), (276, 24.75), 
            (300, 26.625), (324, 28.875), (348, 31.25), (372, 34.0), (396, 36.875)
        ]"""
        expected_sheer = [
            (12, 22.25),
            (36, 20.75),
            (60, 19.875),
            (84, 19.25),
            (108, 19.0),
            (132, 18.875),
            (156, 19.125),
            (180, 19.75),
            (204, 20.625),
            (228, 21.625),
            (252, 23.0),
            (276, 24.75),
            (300, 26.625),
            (324, 28.875),
            (348, 31.25),
            (372, 34.0),
            (396, 36.875),
        ]

        self.assertEqual(17, len(actual_sheer))
        self.assertEqual(expected_sheer, actual_sheer)

        actual_b3 = actual.loft_b3()
        self.assertEqual(13, len(actual_b3))


if __name__ == "__main__":
    unittest.main()
