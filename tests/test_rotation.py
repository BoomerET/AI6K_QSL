from qslstudio.layout import Cardstock, PrinterCalibration
from qslstudio.sheet import Sheet


def make_sheet() -> Sheet:
    stock = Cardstock(
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
    return Sheet(stock, PrinterCalibration())


def test_landscape_corners_fit_first_panel() -> None:
    sheet = make_sheet()
    page_height_pt = 11.0 * 72

    # Landscape card top-left maps to physical panel top-right.
    assert sheet._map_point(page_height_pt, 0, 0, 0, 0) == (3.5 * 72, 11 * 72)

    # Landscape card top-right maps to physical panel bottom-right.
    assert sheet._map_point(page_height_pt, 0, 0, 5.5, 0) == (3.5 * 72, 5.5 * 72)

    # Landscape card bottom-left maps to physical panel top-left.
    assert sheet._map_point(page_height_pt, 0, 0, 0, 3.5) == (0, 11 * 72)


def test_four_panel_origins() -> None:
    sheet = make_sheet()
    assert sheet._panel_origin(0) == (0.0, 0.0)
    assert sheet._panel_origin(1) == (3.5, 0.0)
    assert sheet._panel_origin(2) == (0.0, 5.5)
    assert sheet._panel_origin(3) == (3.5, 5.5)
