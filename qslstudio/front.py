from pathlib import Path

from .layout import Cardstock, PrinterCalibration
from .sheet import Sheet
from .template import TemplateContext, load_card_template


ROOT = Path(__file__).resolve().parents[1]
CARDSTOCK_CONFIG = ROOT / "config" / "cardstock.yaml"
PRINTER_CONFIG = ROOT / "config" / "printer.yaml"
TEMPLATE = ROOT / "templates" / "front.yaml"
OUTPUT = ROOT / "output" / "AI6K_QSL_front.pdf"


def generate(output_path: Path = OUTPUT) -> Path:
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)

    context = TemplateContext(
        {
            "callsign": "AI6K",
            "name": "David Berkompas",
            "location": "Prosper, Texas",
            "tagline": "73 from North Texas",
        }
    )

    sheet = Sheet(stock, printer)

    for _ in range(4):
        sheet.add_card(load_card_template(TEMPLATE, context))

    return sheet.export_pdf(output_path)


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
