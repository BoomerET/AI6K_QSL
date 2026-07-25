from pathlib import Path

from .layout import Cardstock, PrinterCalibration
from .models import QSO, StationProfile
from .sheet import Sheet
from .template import TemplateContext, load_card_template


ROOT = Path(__file__).resolve().parents[1]
CARDSTOCK_CONFIG = ROOT / "config" / "cardstock.yaml"
PRINTER_CONFIG = ROOT / "config" / "printer.yaml"
TEMPLATE = ROOT / "templates" / "back.yaml"
OUTPUT = ROOT / "output" / "AI6K_QSL_back_proof.pdf"


def demo_profile() -> StationProfile:
    return StationProfile(
        callsign="AI6K",
        name="David Berkompas",
        location="Prosper, Texas",
        rig="Icom IC-7300",
        power="100 W",
    )


def demo_qsos() -> list[QSO]:
    return [
        QSO(
            contacted_callsign="W1AW",
            date="2026-07-25",
            time_utc="1915",
            frequency="14.074 MHz",
            mode="FT8",
            rst_sent="-08",
            rst_received="-11",
            remarks="Thanks for the contact.",
        ),
        QSO(
            contacted_callsign="K5ABC",
            date="2026-07-25",
            time_utc="1932",
            frequency="7.190 MHz",
            mode="SSB",
            rst_sent="59",
            rst_received="57",
            remarks="Good signal into North Texas.",
        ),
        QSO(
            contacted_callsign="N0CALL",
            date="2026-07-25",
            time_utc="2004",
            frequency="14.250 MHz",
            mode="SSB",
            rst_sent="57",
            rst_received="55",
            remarks="First QSO with the new card software.",
        ),
        QSO(
            contacted_callsign="VE3XYZ",
            date="2026-07-25",
            time_utc="2038",
            frequency="21.074 MHz",
            mode="FT8",
            rst_sent="-04",
            rst_received="-07",
            remarks="73 from Prosper, Texas.",
        ),
    ]


def generate(output_path: Path = OUTPUT) -> Path:
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)

    profile = demo_profile()
    sheet = Sheet(stock, printer)

    for qso in demo_qsos():
        values = {}
        values.update(profile.to_template_values())
        values.update(qso.to_template_values())

        sheet.add_card(
            load_card_template(
                TEMPLATE,
                TemplateContext(values),
            )
        )

    return sheet.export_pdf(output_path)


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
