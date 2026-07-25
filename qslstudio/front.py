from pathlib import Path

from .card import Card
from .elements import RectangleElement, TextElement
from .layout import Cardstock, PrinterCalibration
from .sheet import Sheet


ROOT = Path(__file__).resolve().parents[1]
CARDSTOCK_CONFIG = ROOT / "config" / "cardstock.yaml"
PRINTER_CONFIG = ROOT / "config" / "printer.yaml"
OUTPUT = ROOT / "output" / "AI6K_QSL_front_proof.pdf"


def build_front_card(card_number: int) -> Card:
    card = Card()

    # Inset proof border. This is not intended for the final artwork.
    card.add(
        RectangleElement(
            x_in=0.20,
            y_in=0.20,
            width_in=3.10,
            height_in=5.10,
            line_width_pt=0.35,
        )
    )

    card.add(
        TextElement(
            text="AI6K",
            x_in=1.75,
            y_in=1.45,
            font_name="Helvetica-Bold",
            font_size=34,
            align="center",
        )
    )

    card.add(
        TextElement(
            text="David Berkompas",
            x_in=1.75,
            y_in=2.00,
            font_name="Helvetica",
            font_size=13,
            align="center",
        )
    )

    card.add(
        TextElement(
            text="Prosper, Texas",
            x_in=1.75,
            y_in=2.27,
            font_name="Helvetica",
            font_size=11,
            align="center",
        )
    )

    card.add(
        TextElement(
            text="73 from North Texas",
            x_in=1.75,
            y_in=4.78,
            font_name="Helvetica-Oblique",
            font_size=9,
            align="center",
        )
    )

    card.add(
        TextElement(
            text=f"Proof card {card_number}",
            x_in=1.75,
            y_in=5.12,
            font_name="Helvetica",
            font_size=6.5,
            align="center",
        )
    )

    return card


def generate(output_path: Path = OUTPUT) -> Path:
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)

    sheet = Sheet(stock, printer)

    for card_number in range(1, 5):
        sheet.add_card(build_front_card(card_number))

    return sheet.export_pdf(output_path)


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
