from pathlib import Path
from .station_config import StationConfig
from .layout import Cardstock, PrinterCalibration
from .sheet import Sheet


ROOT = Path(__file__).resolve().parents[1]
CARDSTOCK_CONFIG = ROOT / "config" / "cardstock.yaml"
PRINTER_CONFIG = ROOT / "config" / "printer.yaml"
TEMPLATE = ROOT / "templates" / "back.yaml"
STATION_CONFIG = ROOT / "config" / "station.yaml"
OUTPUT = ROOT / "output" / "AI6K_QSL_back_proof.pdf"

def generate(output_path: Path = OUTPUT) -> Path:
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)

    sheet = Sheet(stock, printer)

    return sheet.export_pdf(output_path)


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
