from qslstudio.models import StationProfile

from .models import WavelogStationProfile


def station_profile_from_wavelog(
    profile: WavelogStationProfile,
    *,
    name: str,
    rig: str,
    power: str,
    tagline: str = "73 from North Texas",
) -> StationProfile:
    location_parts = [
        profile.city,
        profile.state,
    ]

    location = ", ".join(
        part.strip()
        for part in location_parts
        if part and part.strip()
    )

    if not location:
        location = profile.country or profile.gridsquare

    return StationProfile(
        callsign=profile.callsign,
        name=name,
        location=location,
        rig=rig,
        power=power,
        tagline=tagline,
    )
