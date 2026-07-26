from qslstudio.models import StationProfile
from qslstudio.wavelog.models import WavelogStationProfile


def station_profile_from_wavelog(
    profile: WavelogStationProfile,
    *,
    operator_name: str = "",
    rig: str = "",
    power: str = "",
) -> StationProfile:
    location_parts = [
        part
        for part in (profile.city, profile.state)
        if part
    ]

    return StationProfile(
        callsign=profile.callsign or "",
        name=operator_name,
        location=", ".join(location_parts),
        rig=rig,
        power=power,
    )
