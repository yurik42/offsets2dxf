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
30     1-8-6
28     1-7-7
26     1-7-2
24     1-7-0
22     1-6-7
20     1-7-1
18     1-7-6
16     1-8-5
14     1-9-5
12    1-11-0
10     2-0-6
8      2-2-5
6      2-4-7
4      2-7-2
2     2-10-0
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
