from qslstudio.models import QSO, StationProfile


def test_station_profile_template_values() -> None:
    profile = StationProfile(
        callsign="AI6K",
        name="David Berkompas",
        location="Prosper, Texas",
        rig="Icom IC-7300",
        power="100 W",
    )

    values = profile.to_template_values()

    assert values["callsign"] == "AI6K"
    assert values["rig"] == "Icom IC-7300"


def test_qso_template_values() -> None:
    qso = QSO(
        contacted_callsign="W1AW",
        date="2026-07-25",
        time_utc="1915",
        frequency="14.074 MHz",
        mode="FT8",
        rst_sent="-08",
    )

    values = qso.to_template_values()

    assert values["contacted_callsign"] == "W1AW"
    assert values["mode"] == "FT8"
