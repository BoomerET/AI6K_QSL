from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class StationConfig:
    operator_name: str
    rig: str
    power: str

    @classmethod
    def load(cls, path: Path) -> "StationConfig":
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        return cls(
            operator_name=str(data.get("operator_name", "")),
            rig=str(data.get("rig", "")),
            power=str(data.get("power", "")),
        )