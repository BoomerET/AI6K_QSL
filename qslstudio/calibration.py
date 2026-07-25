from pathlib import Path
from reportlab.lib.colors import black, HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from .layout import Cardstock, PrinterCalibration


ROOT = Path(__file__).resolve().parents[1]
CARDSTOCK_CONFIG = ROOT / "config" / "cardstock.yaml"
PRINTER_CONFIG = ROOT / "config" / "printer.yaml"
OUTPUT = ROOT / "output" / "AI6K_QSL_calibration.pdf"


def top_to_pdf_y(page_height_pt: float, top_in: float) -> float:
    """Convert a top-origin inch coordinate to ReportLab's bottom-origin points."""
    return page_height_pt - (top_in * inch)


def draw_crosshair(c: Canvas, x: float, y: float, arm: float = 0.18 * inch) -> None:
    c.line(x - arm, y, x + arm, y)
    c.line(x, y - arm, x, y + arm)
    c.circle(x, y, 0.055 * inch, stroke=1, fill=0)


def draw_corner_target(c: Canvas, x: float, y: float, sx: int, sy: int) -> None:
    """Draw an L target directed toward a card corner."""
    arm = 0.22 * inch
    c.line(x, y, x + sx * arm, y)
    c.line(x, y, x, y + sy * arm)
    c.circle(x, y, 0.035 * inch, stroke=1, fill=0)


def generate(output_path: Path = OUTPUT) -> Path:
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    page_w = stock.paper_width_in * inch
    page_h = stock.paper_height_in * inch
    c = Canvas(str(output_path), pagesize=(page_w, page_h))

    c.saveState()
    c.translate(printer.x_offset_in * inch, -printer.y_offset_in * inch)
    c.scale(printer.x_scale, printer.y_scale)

    # The targets are inset so they remain printable on a non-borderless printer.
    inset = 0.25
    target_color = HexColor("#222222")
    guide_color = HexColor("#777777")

    c.setStrokeColor(target_color)
    c.setFillColor(black)
    c.setLineWidth(0.7)

    card_number = 1
    for row in range(stock.rows):
        for col in range(stock.columns):
            left = stock.origin_x_in + col * stock.card_width_in
            top = stock.origin_y_in + row * stock.card_height_in
            right = left + stock.card_width_in
            bottom = top + stock.card_height_in

            center_x = (left + stock.card_width_in / 2) * inch
            center_y = top_to_pdf_y(page_h, top + stock.card_height_in / 2)
            draw_crosshair(c, center_x, center_y)

            # Inset corner targets.
            x1 = (left + inset) * inch
            x2 = (right - inset) * inch
            y1 = top_to_pdf_y(page_h, top + inset)
            y2 = top_to_pdf_y(page_h, bottom - inset)

            draw_corner_target(c, x1, y1, +1, -1)
            draw_corner_target(c, x2, y1, -1, -1)
            draw_corner_target(c, x1, y2, +1, +1)
            draw_corner_target(c, x2, y2, -1, +1)

            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(center_x, center_y + 0.30 * inch, f"CARD {card_number}")
            c.setFont("Helvetica", 7.5)
            c.drawCentredString(
                center_x,
                center_y - 0.30 * inch,
                "Center target should be 1.75 in from each side",
            )
            c.drawCentredString(
                center_x,
                center_y - 0.43 * inch,
                "and 2.75 in from top and bottom.",
            )
            card_number += 1

    # Perforation reference lines. These may be clipped near physical page edges,
    # but the central perforations and right-strip boundary should print.
    c.setStrokeColor(guide_color)
    c.setLineWidth(0.35)
    c.setDash(3, 3)
    for x_in in (3.5, 7.0):
        c.line(x_in * inch, 0.25 * inch, x_in * inch, page_h - 0.25 * inch)
    c.line(0.25 * inch, top_to_pdf_y(page_h, 5.5), 7.0 * inch, top_to_pdf_y(page_h, 5.5))
    c.setDash()

    # Right-side calibration notes.
    strip_left = 7.0 * inch
    c.setStrokeColor(black)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(strip_left + 0.75 * inch, page_h - 0.55 * inch, "AI6K QSL")
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(strip_left + 0.75 * inch, page_h - 0.78 * inch, "CALIBRATION v0.1")

    c.setFont("Helvetica", 7)
    notes = [
        "Print at Actual Size / 100%.",
        "Borderless OFF.",
        "Fit or Shrink OFF.",
        "",
        "Measure printed targets",
        "against perforations.",
        "",
        "Record a consistent",
        "horizontal and vertical",
        "offset in printer.yaml.",
    ]
    y = page_h - 1.10 * inch
    for line in notes:
        c.drawCentredString(strip_left + 0.75 * inch, y, line)
        y -= 0.18 * inch

    # One-inch verification ruler in the strip.
    ruler_x = strip_left + 0.30 * inch
    ruler_y = 1.0 * inch
    c.setLineWidth(0.6)
    c.line(ruler_x, ruler_y, ruler_x + 1.0 * inch, ruler_y)
    for eighth in range(9):
        x = ruler_x + eighth * 0.125 * inch
        tick = 0.12 * inch if eighth in (0, 4, 8) else 0.07 * inch
        c.line(x, ruler_y - tick / 2, x, ruler_y + tick / 2)
    c.setFont("Helvetica", 7)
    c.drawCentredString(ruler_x + 0.5 * inch, ruler_y + 0.18 * inch, "This line must measure 1.000 in")

    c.restoreState()
    c.showPage()
    c.save()
    return output_path


def main() -> None:
    path = generate()
    print(f"Created {path}")


if __name__ == "__main__":
    main()
