#
#
#

import ezdxf
import ezdxf.entities
import ezdxf.enums
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

    def buttocks_positions(self):
        """(virtual) Return a dictionary
        E.g.
        {
            "LWL" : 0,
        }
        """
        print("TODO: please define buttocks_positions()")
        return {}

    def waterlines_positions(self):
        """(virtual) Return a dictionary"""
        print("TODO: please define waterline_positions()")
        return {}

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

    def base_offset(self, line_name: str):
        """(virtual) Returns the vertical offset for the given line"""
        return 0

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
                off = self.base_offset(line_name)
                poly_line.append(
                    (stations[pos], s * TableOfOffsets.offset2double(offset) + off)
                )

        return poly_line

    def loft_line_n_sorted(self, n: int):

        def first(t: tuple):
            return t[0]

        poly = self.loft_line_n(n)
        return sorted(poly, key=first)

    def loft_sheer(self):
        """return polyline to represent sheer line"""
        return self.loft_line_n(0)

    def loft_b3(self):
        """return polyline for B3"""
        return self.loft_line_n(1)

    def plot_grid(self, dxf: object):

        stations = self.station_positions()
        xx = stations.values()

        # Draw central line(s)
        for y in self.grid_y_origins():
            dxf.add_grid_polyline([(min(xx) - 12, y), (max(xx) + 12, y)])

        # draw station lines
        bottom_y, top_y = self.drawing_area_vertical_borders()

        for x in xx:
            dxf.add_grid_polyline([(x, bottom_y), (x, top_y)])

        for y in self.grid_y_origins():
            # place labels offset-ed by (1,1) from the waterline and
            # the station vertical intersection
            for s, x in stations.items():
                dxf.text((x + 1, y + 1), s)

        # waterlines
        for wl, wl_y in self.waterlines_positions().items():
            print("Waterline: ", wl, "at", wl_y)
            dxf.add_grid_polyline([(min(xx) - 12, wl_y), (max(xx) + 12, wl_y)])
            dxf.text((min(xx) - 12 + 1, wl_y + 1), wl)
            dxf.text((max(xx) + 12 - 1, wl_y + 1), wl)

        # buttocks
        buttocks_origin = 0
        if len(self.grid_y_origins()) > 1:
            buttocks_origin = self.grid_y_origins()[1]
        for wl, wl_y in self.buttocks_positions().items():
            print("Buttocks line: ", wl, "at", wl_y)
            wl_y += buttocks_origin
            dxf.add_grid_polyline([(min(xx) - 12, wl_y), (max(xx) + 12, wl_y)])
            dxf.text((min(xx) - 12 + 1, wl_y + 1), wl)
            dxf.text((max(xx) + 12 - 1, wl_y + 1), wl)

    def drawing_area_vertical_borders(self):
        """(virtual) return (bottom, top)"""
        return (-12 * 10, 12 * 10)

    def grid_y_origins(self):
        """(virtual) returns y-coordinate list of the horizontal lines in the grid"""
        return [0.0]

    def loft_body_line(self: object, station: str, width: list, heights: list):
        """return a polylie to represent a body line at the given station"""
        poly = []

        print("TODO: loft_body_line(...) is not implemented yet")

        return poly

        # the first point is expected on the sheer
        poly = []


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
        self._doc.layers.add(name="text", color=3)

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
        if exception_val is not None:
            raise Exception(str(exception_val))

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

    def text(self, xy: tuple, txt: str):
        """Add text to the tet layer

        # Using a predefined text style:
        msp.add_text(
            "Text Style Example: Liberation Serif",
            height=0.35,
            dxfattribs={"style": "LiberationSerif"}
        ).set_placement((2, 6), align=TextEntityAlignment.LEFT)
        """
        self._msp.add_text(txt, height=1.0, dxfattribs={"layer": "text"}).set_placement(
            xy, align=ezdxf.enums.TextEntityAlignment.LEFT
        )
