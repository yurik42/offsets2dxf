#
#
#

import context
from context import table_of_offsets

import os


#
# Model implementation spicific for the sample data
#
class ProjectBlueMoon(table_of_offsets.Model):
    def __init__(self):
        super().__init__(
            os.path.join(
                os.path.dirname(__file__),
                "../sample_data_too/offset_table_blue_moon.csv",
            )
        )
        # fmt: off
        self.set_under_waterline(
            {
            }
        )
        # fmt: on
        self._y_lwl = 4 * 12 + 1 + 7.0 / 8.0  # 4-1-7
        self._y0 = 0.0
        self._y1 = -120.0
        pass

    def station_positions(self):
        """Return a dictionary of station positions
        waterlines 0-9-0
        stations   3-0-0
        butts      1-0-0
        7..8       1-8-4
        """
        station_positions = {}
        for c in self._too.columns:
            if c == "#":
                pass
            elif c == "TRAN.":
                station_positions[c] = 0.0
            elif c == "8":
                station_positions[c] = 3 * 12 - 20.5  #  1-8-4 == 20.5
            else:
                assert c.isdecimal()
                station_positions[c] = (8 - int(c)) * 12 * 3  # 1' == 12" (inches)
        return station_positions

    def base_offset(self, line_name: str):
        """(virtual) Returns the vertical offset for the given line"""
        if line_name in ["LWL to SHEER", "LWL to DECK EDG"]:
            return self._y_lwl

        # the line_name is one of 'plane' lines
        if line_name in [
            "SHEER",
            "WL 2A",
            "WL 1A",
            "LWL",
            "WL 1B",
            "WL 2B",
            "RABBET",
            "KEEL",
            "BALLAST TOP",
        ]:
            return self._y1

        return 0

    def grid_y_origins(self):
        """(virtual) we want two horizontal (central) grid lines"""
        return [0, -10 * 12.0]

    def waterlines_positions(self):
        wl = {
            "WL 2A": 18.0,
            "WL 1A": 9.0,
            "LWL": 0.0,
            "WL 1B": -9.0,
            "WL 2B": -18.0,
        }
        for k in wl:
            wl[k] += self._y_lwl
        return wl

    def buttocks_positions(self):
        return {"BASE TO B-3": 36.0, "BASE TO B-2": 24.0, "BASE TO B-1": 12.0}

    def grid_y_origins(self):
        """(virtual): central lines will be drawn here"""
        return [self._y0, self._y1]

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF(filename_dxf) as dxf:
            self.plot_grid(dxf)

            dxf.add_red_polyline(self.loft_line_n(0))
            dxf.add_red_polyline(self.loft_line_n(1))
            dxf.add_red_polyline(self.loft_line_n(2))
            dxf.add_red_polyline(self.loft_line_n(3))
            dxf.add_red_polyline(self.loft_line_n(4))
            dxf.add_red_polyline(self.loft_line_n(5))
            dxf.add_red_polyline(self.loft_line_n(6))
            dxf.add_red_polyline(self.loft_line_n(7))
            dxf.add_red_polyline(self.loft_line_n(8))
            #
            # now half-bradth
            #
            dxf.add_red_polyline(self.loft_line_n(9))
            dxf.add_red_polyline(self.loft_line_n(10))
            dxf.add_red_polyline(self.loft_line_n(11))
            dxf.add_red_polyline(self.loft_line_n(12))
            dxf.add_red_polyline(self.loft_line_n(13))
            dxf.add_red_polyline(self.loft_line_n(14))


if __name__ == "__main__":
    proj = ProjectBlueMoon()
    proj.save_model_as("test_project_blue_moon.dxf")
    print("Saved as:", os.path.abspath("test_project_blue_moon.dxf"))

# end of file
