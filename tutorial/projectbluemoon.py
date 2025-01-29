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
                "../sample_data/offset_table_blue_moon.local.csv",
            )
        )
        # fmt: off
        self.set_under_waterline(
            {
            }
        )
        # fmt: on
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
            return 4 * 12 + 1 + 7.0 / 8.0  # 4-1-7

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
            return -10 * 12.0

        return 0

    def plot_grid_more(self, dxf: object):
        """Draw second line for plane views"""
        stations = self.station_positions()
        xx = stations.values()

        # Draw a "waterline"
        dxf.add_grid_polyline([(min(xx) - 12, -10 * 12.0), (max(xx) + 12, -10 * 12.0)])

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF(filename_dxf) as dxf:
            self.plot_grid(dxf)
            self.plot_grid_more(dxf)

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
            # now half-breadth
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
