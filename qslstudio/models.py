from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class StationProfile:
    callsign: str
    name: str
    location: str
    rig: str
    power: str
    tagline: str = "73 from North Texas"

    def to_template_values(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class QSO:
    contacted_callsign: str
    date: str
    time_utc: str
    frequency: str
    mode: str
    rst_sent: str
    rst_received: str = ""
    remarks: str = ""
    qsl_message: str = "TNX QSO"

    def to_template_values(self) -> dict[str, str]:
        return asdict(self)
