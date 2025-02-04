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
                os.path.dirname(__file__), "../sample_data_too/offset_table_181.csv"
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
        self._y0 = 0.0
        self._y1 = -100.0
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

    def waterlines_positions(self):
        return {
            '24" LL': 24.0,
            '16" LL': 16.0,
            '8" LL': 8.0,
            "DWL": 0.0,
            '8" DL': -8,
            '16" DL': -16.0,
        }

    def buttocks_positions(self):
        return {
            '36" Buttock': 36.0,
            '24" Buttock': 24.0,
            '12" Buttock': 12.0,
        }

    def base_offset(self, line_name):
        if line_name in [
            "Sheerline",
            '24" LL',
            '16" LL',
            '8" LL',
            "DWL",
            '8" DL',
            '16" DL',
            "Rabbet Line",
        ]:
            return self._y1
        return self._y0

    def grid_y_origins(self):
        return [self._y0, self._y1]

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF("test_project181.dxf") as dxf:
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
