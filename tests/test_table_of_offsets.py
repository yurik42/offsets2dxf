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


if __name__ == "__main__":
    unittest.main()
