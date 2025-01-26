#
#
#

import ezdxf
import ezdxf.entities
import numpy
import pandas
import math

__version__ = "0.5.0"


class TableOfOffsets:
    def __init__(self):
        pass

    """#      Sheer
33       NaN
32    1-10-2
...
0      3-0-7
Name: 0, dtype: object
"""

    @staticmethod
    def verify_triplet(w: list):
        return True

    @staticmethod
    def offset2double(triplet: str):
        delta = 0
        if triplet[-1] == "-":
            delta = -1.0 / 16
            triplet = triplet[:-1]
        elif triplet[-1] == "+":
            delta = 1.0 / 16.0
            triplet = triplet[:-1]

        w = triplet.split("-")
        TableOfOffsets.verify_triplet(w)
        d = 0
        if len(w) == 3:
            d = int(w[0]) * 12.0 + int(w[1]) + int(w[2]) / 8.0
        elif len(w) == 2:
            d = int(w[0]) * 12.0 + int(w[1])
        elif len(w) == 1:
            d = int(w[0]) * 12.0
        else:
            raise Exception("bad offset format")
        return d + delta


class Model:
    def __init__(self: object, _filename_csv: str):
        self._filename_csv = _filename_csv
        self._too = pandas.read_csv(self._filename_csv)
        self._under_waterline = {}
        pass

    def set_under_waterline(self, d: dict):
        self._under_waterline = d

    def units(self):
        return "inch"

    def station_positions(self):
        """Return a dictionary of station positions"""
        station_positions = {}
        for c in self._too.columns:
            if c == "#":
                pass
            else:
                assert c.isdecimal()
                station_positions[c] = (33 - int(c)) * 12  # 1' == 12" (inches)
        return station_positions

    def offset_sign(self, station: str, line: str):
        """Returns either 1 or -1
        The function is used if offsets are negative below waterline

        {
            "B 3" : [ "33" , "20", ... ],
        }
        """
        if not line in self._under_waterline:
            return 1
        under = self._under_waterline[line]
        return -1 if station in under else 1

    def loft_line_n(self, n: int):
        """return polyline for n-th line"""
        line_offsets = self._too.loc[n]
        stations = self.station_positions()

        poly_line = list()
        line_name = line_offsets["#"]
        for pos in stations:
            offset = line_offsets[pos]
            if type(offset) is str:
                s = self.offset_sign(pos, line_name)
                poly_line.append(
                    (stations[pos], s * TableOfOffsets.offset2double(offset))
                )

        return poly_line

    def loft_sheer(self):
        """return polyline to represent sheer line"""
        return self.loft_line_n(0)

    def loft_b3(self):
        """return polyline for B3"""
        return self.loft_line_n(1)

    def plot_grid(self, dxf: object):

        xx = self.station_positions().values()

        # Draw a "waterline"
        dxf.add_grid_polyline([(min(xx) - 12, 0), (max(xx) + 12, 0)])

        # draw station lines
        # TODO: add function to compute bounding box
        top_y = 12 * 10
        bottom_y = -12 * 10

        for x in xx:
            dxf.add_grid_polyline([(x, bottom_y), (x, top_y)])


class DXF:
    """
    ACI colors
    1: Red
    2: Yellow
    3: Green
    4: Cyan
    5: Blue
    6: Magenta
    7: White or black
    """

    def __init__(self, output_dxf: str):
        self._output_dxf = output_dxf
        self._doc = ezdxf.new("R2010")
        self._msp = self._doc.modelspace()
        self._doc.layers.add(name="grid", color=6)
        self._doc.layers.add(name="red", color=1)

    def __enter__(self):
        # print("Enter with:", self._output_dxf)
        return self

    def __exit__(self, exception_type, exception_val, trace):
        # Exit logic here, called at exit of with block
        # print("Exit with:", self._output_dxf)
        # print(type(exception_type), type(exception_val), type(trace))
        # print("exception_type:", exception_type)
        # print("exception_val:", exception_val)

        self.close()

        return True

    def add_polyline(self, poly: list):
        self._msp.add_polyline2d(poly)

    def add_red_polyline(self, poly: list):
        self._msp.add_polyline2d(poly, dxfattribs={"layer": "red"})

    def add_grid_polyline(self, poly: list):
        self._msp.add_polyline2d(poly, dxfattribs={"layer": "grid"})

    def close(self):
        if self._doc is not None:
            self._doc.saveas(self._output_dxf)
            self._doc = None
            self._msp = None
