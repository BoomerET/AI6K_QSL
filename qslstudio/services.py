from datetime import datetime
from pathlib import Path

from .adif import parse_adif, qso_from_adif
from .back import CARDSTOCK_CONFIG, PRINTER_CONFIG, TEMPLATE
from .layout import Cardstock, PrinterCalibration
from .models import QSO, StationProfile
from .sheet import Sheet
from .template import TemplateContext, load_card_template
from .wavelog.adapter import station_profile_from_wavelog
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig


ROOT = Path(__file__).resolve().parents[1]
WAVELOG_CONFIG = ROOT / "config" / "config.yaml"


def qso_sort_key(record: dict[str, str]) -> datetime:
    date = record.get("QSO_DATE", "00010101")
    time = record.get("TIME_ON", "000000").ljust(6, "0")[:6]

    try:
        return datetime.strptime(
            f"{date}{time}",
            "%Y%m%d%H%M%S",
        )
    except ValueError:
        return datetime.min


def fetch_recent_qsos(
    limit: int = 50,
) -> tuple[StationProfile, list[QSO]]:
    """Download recent QSOs and the active station profile from Wavelog."""

    config = WavelogConfig.load(WAVELOG_CONFIG)
    client = WavelogClient(config)

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

    export = client.export_adif(
        station_id=wavelog_profile.station_id,
    )

    records = parse_adif(export.adif)

    if not records:
        raise RuntimeError("Wavelog returned no QSO records.")

    recent_records = sorted(
        records,
        key=qso_sort_key,
        reverse=True,
    )[:limit]

    qsos = [
        qso_from_adif(record)
        for record in recent_records
    ]

    profile = station_profile_from_wavelog(
        wavelog_profile,
        operator_name="David Berkompas",
        rig="Icom IC-7300",
        power="100 W",
    )

    return profile, qsos


def generate_back_pdf(
    qsos: list[QSO],
    profile: StationProfile,
    output_path: Path,
) -> Path:
    """Render selected QSOs into a printable back-side PDF."""

    if not qsos:
        raise ValueError("At least one QSO is required.")

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

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return sheet.export_pdf(output_path)
