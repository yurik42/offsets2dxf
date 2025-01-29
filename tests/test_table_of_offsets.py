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

        actual_bottom, actual_top = actual.drawing_area_vertical_borders()
        self.assertEqual(-120, actual_bottom)
        self.assertEqual(120, actual_top)

    def test_DXF(self):
        # clean up the workspace
        if os.path.exists("test_DXF.dxf"):
            os.remove("test_DXF.dxf")
        self.assertFalse(os.path.exists("test_DXF.dxf"))

        # Test:
        # - create dxf object
        # - close
        # ASSERT: output file is created
        actual_dxf = table_of_offsets.DXF("test_DXF.dxf")
        actual_dxf.close()
        self.assertTrue(os.path.exists("test_DXF.dxf"))

        # - remove output
        os.remove("test_DXF.dxf")
        self.assertFalse(os.path.exists("test_DXF.dxf"))

        # close the object
        # ASSERT: output is not created
        actual_dxf.close()
        self.assertFalse(os.path.exists("test_DXF.dxf"))

    def test_DXF_2(self):
        """Test __exit__ method"""
        # clean up the workspace
        if os.path.exists("test_DXF_2.dxf"):
            os.remove("test_DXF_2.dxf")
        self.assertFalse(os.path.exists("test_DXF_2.dxf"))

        # Test:
        # - create dxf object
        # - call __exit__
        # ASSERT: output file is created
        with table_of_offsets.DXF("test_DXF_2.dxf") as actual_dxf:
            self.assertIs(type(actual_dxf), table_of_offsets.DXF)
            actual_dxf.add_grid_polyline([(0, 0), (10, 10)])

        self.assertTrue(os.path.exists("test_DXF_2.dxf"))


if __name__ == "__main__":
    unittest.main()
