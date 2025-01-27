#
#
#

import context
from context import table_of_offsets

import os


#
# Model implementation spicific for the sample data
#
class Project181(table_of_offsets.Model):
    def __init__(self):
        super().__init__(
            os.path.join(
                os.path.dirname(__file__), "../sample_data/offset_table_181.local.csv"
            )
        )
        # fmt: off
        self.set_under_waterline(
            { 
                '36" Buttock': [ "5" ],
                '24" Buttock': [ "3", "4", "5", "6", "7" ],
                '12" Buttock': [ "2", "3", "4", "5", "6", "7" ],
                'Rabbet': [ "1", "2", "3", "4", "5", "6", "7" ],
                'Profile': [ "1", "2", "3", "4", "5", "6", "7" ],
            }
        )
        # fmt: on
        pass

    def station_positions(self):
        """Return a dictionary of station positions"""
        station_positions = {}
        for c in self._too.columns:
            if c == "#":
                pass
            elif c == "AP":
                station_positions[c] = 0.0
            elif c == "FP":
                station_positions[c] = 24 * 9
            else:
                assert c.isdecimal()
                station_positions[c] = (9 - int(c)) * 24  # 1' == 12" (inches)
        return station_positions

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF("test_model181.dxf") as dxf:
            self.plot_grid(dxf)

            dxf.add_red_polyline(self.loft_line_n_sorted(0))
            dxf.add_red_polyline(self.loft_line_n_sorted(1))
            dxf.add_red_polyline(self.loft_line_n_sorted(2))
            dxf.add_red_polyline(self.loft_line_n_sorted(3))
            dxf.add_red_polyline(self.loft_line_n_sorted(4))
            #
            dxf.add_red_polyline(self.loft_line_n_sorted(6))


if __name__ == "__main__":
    proj = Project181()

    print(proj.station_positions())

    proj.save_model_as("test_project181.dxf")
    print("Saved as:", os.path.abspath("test_project181.dxf"))

# end of file
