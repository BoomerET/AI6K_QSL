from qslstudio.layout import Cardstock, PrinterCalibration
from qslstudio.sheet import Sheet


def make_stock() -> Cardstock:
    return Cardstock(
        paper_width_in=8.5,
        paper_height_in=11.0,
        card_width_in=3.5,
        card_height_in=5.5,
        columns=2,
        rows=2,
        origin_x_in=0.0,
        origin_y_in=0.0,
        strip_width_in=1.5,
    )


def test_panel_origins() -> None:
    sheet = Sheet(make_stock(), PrinterCalibration())

    assert sheet._panel_origin(0) == (0.0, 0.0)
    assert sheet._panel_origin(1) == (3.5, 0.0)
    assert sheet._panel_origin(2) == (0.0, 5.5)
    assert sheet._panel_origin(3) == (3.5, 5.5)
