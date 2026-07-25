from dataclasses import dataclass


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
    def from_api(cls, data: dict) -> "WavelogStationProfile":
        return cls(
            station_id=int(data["station_id"]),
            profile_name=data["station_profile_name"],
            callsign=data["station_callsign"],
            gridsquare=data["station_gridsquare"],
            city=data["station_city"],
            state=data["station_state"],
            country=data["station_country"],
            active=data["station_active"] == "1",
            uuid=data["station_uuid"],
        )