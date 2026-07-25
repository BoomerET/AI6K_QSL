from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class Cardstock:
    paper_width_in: float
    paper_height_in: float
    card_width_in: float
    card_height_in: float
    columns: int
    rows: int
    origin_x_in: float
    origin_y_in: float
    strip_width_in: float

    @classmethod
    def load(cls, path: Path) -> "Cardstock":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        paper = data["paper"]
        card = data["card"]
        strip = data["unused_strip"]

        return cls(
            paper_width_in=float(paper["width_in"]),
            paper_height_in=float(paper["height_in"]),
            card_width_in=float(card["width_in"]),
            card_height_in=float(card["height_in"]),
            columns=int(card["columns"]),
            rows=int(card["rows"]),
            origin_x_in=float(card["origin_x_in"]),
            origin_y_in=float(card["origin_y_in"]),
            strip_width_in=float(strip["width_in"]),
        )


@dataclass(frozen=True)
class PrinterCalibration:
    x_offset_in: float = 0.0
    y_offset_in: float = 0.0
    x_scale: float = 1.0
    y_scale: float = 1.0

    @classmethod
    def load(cls, path: Path) -> "PrinterCalibration":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))["printer"]
        return cls(
            x_offset_in=float(data.get("x_offset_in", 0.0)),
            y_offset_in=float(data.get("y_offset_in", 0.0)),
            x_scale=float(data.get("x_scale", 1.0)),
            y_scale=float(data.get("y_scale", 1.0)),
        )
