from pathlib import Path

from .adif import parse_adif, qso_from_adif
from .back import (
    CARDSTOCK_CONFIG,
    OUTPUT,
    PRINTER_CONFIG,
    TEMPLATE,
    demo_profile,
)
from .layout import Cardstock, PrinterCalibration
from .sheet import Sheet
from .template import TemplateContext, load_card_template
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig


ROOT = Path(__file__).resolve().parents[1]
LIVE_OUTPUT = ROOT / "output" / "AI6K_QSL_live_back.pdf"


def generate(output_path: Path = LIVE_OUTPUT) -> Path:
    #config = WavelogConfig.load()
    config = WavelogConfig.load(Path("config/config.yaml"))
    client = WavelogClient(config)

    print("Downloading QSOs from Wavelog...")

    export = client.export_adif(station_id=1)
    records = parse_adif(export.adif)

    if not records:
        raise RuntimeError("Wavelog returned no QSO records.")

    # Start with one real QSO for the end-to-end test.
    profile = demo_profile()

    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)
    sheet = Sheet(stock, printer)

    qsos = [
        qso_from_adif(record)
        for record in reversed(records[-4:])
    ]

    for qso in qsos:
        values = {}
        values.update(profile.to_template_values())
        values.update(qso.to_template_values())

        sheet.add_card(
            load_card_template(
                TEMPLATE,
                TemplateContext(values),
            )
        )

        print(
            f"Rendering {qso.contacted_callsign} "
            f"from {qso.date} at {qso.time_utc} UTC..."
        )

    return sheet.export_pdf(output_path)


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
