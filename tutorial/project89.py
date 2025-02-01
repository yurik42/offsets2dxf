#
#
#

import context
from context import table_of_offsets

import os


#
# Model implementation spicific for the sample data
#
class Project89(table_of_offsets.Model):
    def __init__(self):
        super().__init__(
            os.path.join(os.path.dirname(__file__), "../sample_data/offset_table.csv")
        )
        # fmt: off
        self.set_under_waterline(
            {
                "B 3'": [
                    "24", "22", "20", "18", "16", "14", "12",
                ],
                "B 2'": [
                    "26", "24", "22", "20", "18", "16", "14", "12", "10", "8"
                ],
                "B 1'": [
                    "28", "26", "24", "22", "20", "18", "16", "14", "12", "10", "8", "6"
                ],
                "Rabbet": [ 
                    "30", "28", "26", "24", "22", "20", "18",
                    "16", "14", "12", "10",  "8",  "6",  "4",
                ],
                "Profile": [
                    "30", "28", "26", "24", "22", "20", "18",
                    "16", "14", "12", "10",  "8",  "6",  "4",  "2",
                ],
            }
        )
        # fmt: on
        pass

    def base_offset(self, line_name: str):
        if line_name in [
            "1/2w Deck",
            "WL + 2'",
            "WL + 1'",
            'WL + 6"',
            "LWL",
            'WL - 6"',
            "WL - 1'",
            "WL - 2'",
            "WL - 3'",
            "WL - 4'",
            "Rabbet Plan",
            "Profile Plan",
        ]:
            return 10 * 12.0  #
        return 0

    def buttocks_positions(self):
        return {"B 3'": 3 * 12.0, "B 2'": 2 * 12.0, "B 1'": 12 * 1.0}

    def waterlines_positions(self):
        return {
            "WL + 2'": 2 * 12.0,
            "WL + 1'": 12.0,
            'WL + 6"': 6.0,
            "LWL": 0.0,
            'WL - 6"': -6.0,
            "WL - 1'": -12.0,
            "WL - 2'": -24.0,
            "WL - 3'": -36.0,
            "WL - 4'": -4 * 12,
        }

    def drawing_area_vertical_borders(self):
        """(virtual)"""
        return (-12 * 10, 20 * 12)

    def grid_y_origins(self):
        """(virtual) we want two horizontal grid lines"""
        return [0, 10 * 12.0]

    def save_model_as(self, filename_dxf: str):
        with table_of_offsets.DXF(filename_dxf) as dxf:
            self.plot_grid(dxf)

            dxf.add_red_polyline(self.loft_line_n(0))
            dxf.add_red_polyline(self.loft_line_n(1))
            dxf.add_red_polyline(self.loft_line_n(2))
            dxf.add_red_polyline(self.loft_line_n(3))
            dxf.add_red_polyline(self.loft_line_n(4))
            #
            dxf.add_red_polyline(self.loft_line_n(6))
            dxf.add_red_polyline(self.loft_line_n(7))
            dxf.add_red_polyline(self.loft_line_n(8))
            dxf.add_red_polyline(self.loft_line_n(9))
            dxf.add_red_polyline(self.loft_line_n(10))
            dxf.add_red_polyline(self.loft_line_n(11))
            dxf.add_red_polyline(self.loft_line_n(12))

            heights = ["Sheer", "B 3'", "B 2'", "B 1'", "Rabbet", "Profile"]
            widths = [
                "1/2w Deck",
                "WL + 2'",
                "WL + 1'",
                'WL + 6"',
                "LWL",
                'WL - 6"',
                "WL - 1'",
                "WL - 2'",
                "WL - 3'",
                "WL - 4'",
                "Rabbet Plan",
                "Profile Plan",
            ]
            dxf.add_red_polyline(self.loft_body_line("18", widths, heights))


if __name__ == "__main__":
    proj = Project89()
    proj.save_model_as("test_project89.dxf")
    print("Saved as:", os.path.abspath("test_project89.dxf"))

# end of file
