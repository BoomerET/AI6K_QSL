from datetime import datetime
from pathlib import Path

from .adif import parse_adif, qso_from_adif
from .models import QSO, StationProfile
from .print_profiles import (
    get_default_print_profile_id,
    get_print_profile,
)
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

def test_wavelog_connection(config: WavelogConfig) -> str:
    client = WavelogClient(config)
    version = client.get_version()
    station_profiles = client.get_station_profiles()

    if not station_profiles:
        raise RuntimeError(
            "Connected, but Wavelog returned no station profiles."
        )

    return version

def fetch_recent_qsos(
    limit: int = 50,
) -> tuple[StationProfile, list[QSO]]:
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
    print_profile_id: str | None = None,
) -> Path:
    selected_profile_id = print_profile_id or get_default_print_profile_id()
    print_profile = get_print_profile(selected_profile_id)
    return print_profile.layout.render(
        qsos,
        profile,
        output_path,
        printer_config=print_profile.printer_config,
    )

