from dataclasses import dataclass
import requests
from .config import WavelogConfig
from .models import WavelogStationProfile

@dataclass
class WavelogClient:
    config:WavelogConfig

    def _post_json(self, endpoint, payload):
        r = requests.post(
            f"{self.config.url.rstrip('/')}/{endpoint}",
            json=payload,
            timeout=30,
        )

        r.raise_for_status()
        return r.json()

    def _post_key(self, endpoint):
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

    #def get_station_profiles(self):
    #    url = (
    #        f"{self.config.url.rstrip('/')}"
    #        f"/api/station_info/{self.config.api_key}"
    #    )

    #    r = requests.post(url, timeout=30)

    #    print(f"POST {r.request.url}")
    #    print(f"Status: {r.status_code}")
    #    print(r.text)

    #    r.raise_for_status()
    #    data = r.json()
    #    return [WavelogStationProfile.from_api(x) for x in data]

    def get_station_profiles(self):
        data = self._post_key("api/station_info")
        return [WavelogStationProfile.from_api(x) for x in data]

    def export_adif(self,fetch_from_id:int|None=None):
        body={"key":self.config.api_key}
        if fetch_from_id is not None:
            body["fetchfromid"]=fetch_from_id
        return self._post("api/get_contacts_adif",body)
