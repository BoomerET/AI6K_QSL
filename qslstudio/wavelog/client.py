from __future__ import annotations
from dataclasses import dataclass
import requests
from .config import WavelogConfig
from .models import WavelogAdifExport, WavelogStationProfile

@dataclass(slots=True)
class WavelogClient:
    config: WavelogConfig

    #def _post_json(self, endpoint: str, payload: dict) -> dict:
    #    r = requests.post(
    #        f"{self.config.url.rstrip('/')}/{endpoint}",
    #        json=payload,
    #        timeout=30,
    #    )

    #    r.raise_for_status()
    #    return r.json()
    def _post_json(self, endpoint, payload):
        r = requests.post(
            f"{self.config.url.rstrip('/')}/{endpoint}",
            json=payload,
            timeout=30,
        )

        if not r.ok:
            print(f"Status: {r.status_code}")
            print(r.text)

        r.raise_for_status()
        return r.json()

    def _post_key(self, endpoint: str) -> list[dict]:
        url = (
            f"{self.config.url.rstrip('/')}"
            f"/{endpoint}/{self.config.api_key}"
        )

        r = requests.post(
            url,
            timeout=30,
        )

        r.raise_for_status()
        return r.json()

    def get_version(self) -> str:
        data = self._post_json(
            "api/version",
            {"key": self.config.api_key},
        )
        return data["version"]

    def get_station_profiles(self) -> list[WavelogStationProfile]:
        data = self._post_key("api/station_info")
        return [WavelogStationProfile.from_api(x) for x in data]

    def export_adif(
        self,
        station_id: int,
        fetch_from_id: int = 0,
    ) -> WavelogAdifExport:
        body = {
            "key": self.config.api_key,
            "station_id": station_id,
            "fetchfromid": fetch_from_id,
        }
    
        data = self._post_json(
            "api/get_contacts_adif",
            body,
        )
    
        return WavelogAdifExport.from_api(data)
