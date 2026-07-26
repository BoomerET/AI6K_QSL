from pathlib import Path
from datetime import datetime
from .adif import parse_adif, qso_from_adif
from .back import (
    CARDSTOCK_CONFIG,
    PRINTER_CONFIG,
    TEMPLATE,
)
from .layout import Cardstock, PrinterCalibration
from .sheet import Sheet
from .template import TemplateContext, load_card_template
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig
from .wavelog.adapter import station_profile_from_wavelog


ROOT = Path(__file__).resolve().parents[1]
LIVE_OUTPUT = ROOT / "output" / "AI6K_QSL_live_back.pdf"

def qso_sort_key(record: dict[str, str]) -> datetime:
    date = record.get("QSO_DATE", "00010101")
    time = record.get("TIME_ON", "000000").ljust(6, "0")[:6]

    try:
        return datetime.strptime(f"{date}{time}", "%Y%m%d%H%M%S")
    except ValueError:
        return datetime.min

def generate(output_path: Path = LIVE_OUTPUT) -> Path:
    #config = WavelogConfig.load()
    config = WavelogConfig.load(Path("config/config.yaml"))
    client = WavelogClient(config)

    print("Downloading QSOs from Wavelog...")

    station_profiles = client.get_station_profiles()

    if not station_profiles:
        raise RuntimeError("Wavelog returned no station profiles.")

    wavelog_profile = next(
        (
            station_profile
            for station_profile in station_profiles
            if station_profile.active
        ),
        station_profiles[0],
    )

    print(
        f"Using station profile: "
        f"{wavelog_profile.profile_name} "
        f"({wavelog_profile.callsign})"
    )

    export = client.export_adif(
        station_id=wavelog_profile.station_id,
    )
    
    records = parse_adif(export.adif)
    
    if not records:
        raise RuntimeError("Wavelog returned no QSO records.")
    
    newest_records = sorted(
        records,
        key=qso_sort_key,
        reverse=True,
    )[:4]
    
    qsos = [qso_from_adif(record) for record in newest_records]

    profile = station_profile_from_wavelog(
        wavelog_profile,
        operator_name="David Berkompas",
        rig="Icom IC-7300",
        power="100 W",
    )
    
    stock = Cardstock.load(CARDSTOCK_CONFIG)
    printer = PrinterCalibration.load(PRINTER_CONFIG)
    sheet = Sheet(stock, printer)
    
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
