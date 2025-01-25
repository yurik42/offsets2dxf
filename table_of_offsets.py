#
#
#

import ezdxf
import numpy
import pandas

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
        pass

    def units(self):
        return "inch"

    def station_positions(self):
        """Return a list of station positions"""
        station_positions = {}
        for c in self._too.columns:
            if c == "#":
                pass
            else:
                assert c.isdecimal()
                station_positions[c] = (33 - int(c)) * 12  # 1' == 12" (inches)
        return station_positions
