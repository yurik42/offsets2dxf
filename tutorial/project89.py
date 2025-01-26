#
#
#

import context
from context import table_of_offsets

import os


class Project89(table_of_offsets.Model):
    def __init__(self):
        super().__init__(
            os.path.join(os.path.dirname(__file__), "../sample_data/offset_table.csv")
        )
        # fmt: off
        self.set_under_waterline(
            {
                "B 3'": [
                    "24", "22", "20", "18", "16", "14", "12", "10",
                ],
                "Rabbet": [ 
                    "30", "28", "26", "24", "22", "20", "18",
                    "16", "14", "12", "10",  "8",  "6",  "4",  "2",
                ],
                "Profile": [
                    "30", "28", "26", "24", "22", "20", "18",
                    "16", "14", "12", "10",  "8",  "6",  "4",  "2",
                ],
            }
        )
        # fmt: on
        pass

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF("test_model89.dxf") as dxf:
            self.plot_grid(dxf)

            dxf.add_red_polyline(self.loft_line_n(0))
            dxf.add_red_polyline(self.loft_line_n(1))
            dxf.add_polyline(self.loft_line_n(2))
            dxf.add_polyline(self.loft_line_n(3))
            dxf.add_polyline(self.loft_line_n(4))
            #
            dxf.add_red_polyline(self.loft_line_n(6))


if __name__ == "__main__":
    proj = Project89()
    proj.save_model_as("test_project89.dxf")
    print("Saved as:", os.path.abspath("test_project89.dxf"))

# end of file
