from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WavelogStationProfile:
    station_id: int
    profile_name: str
    callsign: str
    gridsquare: str
    city: str
    state: str
    country: str
    active: bool
    uuid: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "WavelogStationProfile":
        return cls(
            station_id=int(data["station_id"]),
            profile_name=data.get("station_profile_name", ""),
            callsign=data.get("station_callsign", ""),
            gridsquare=data.get("station_gridsquare", ""),
            city=data.get("station_city", ""),
            state=data.get("station_state", ""),
            country=data.get("station_country", ""),
            active=bool(data.get("station_active", False)),
            uuid=data.get("station_uuid", ""),
        )

    def __str__(self) -> str:
        active = " (active)" if self.active else ""
        return (
            f"{self.station_id}: "
            f"{self.profile_name} "
            f"({self.callsign}){active}"
        )


@dataclass(slots=True)
class WavelogAdifExport:
    status: str
    message: str
    last_fetched_id: int
    exported_qsos: int
    adif: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "WavelogAdifExport":
        return cls(
            status=str(data.get("status", "")),
            message=str(data.get("message", "")),
            last_fetched_id=int(data.get("lastfetchedid", 0)),
            exported_qsos=int(data.get("exported_qsos", 0)),
            adif=str(data.get("adif", "")),
        )