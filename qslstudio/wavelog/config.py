from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class WavelogConfig:
    url:str
    api_key:str

    @classmethod
    def load(cls,path:Path):
        data=yaml.safe_load(path.read_text())
        wl=data["wavelog"]
        return cls(url=wl["url"],api_key=wl["api_key"])
