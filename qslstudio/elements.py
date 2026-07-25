from dataclasses import dataclass
from typing import Literal

HorizontalAlign = Literal["left", "center", "right"]


@dataclass(frozen=True)
class TextElement:
    text: str
    x_in: float
    y_in: float
    font_name: str = "Helvetica"
    font_size: float = 12.0
    align: HorizontalAlign = "left"


@dataclass(frozen=True)
class LineElement:
    x1_in: float
    y1_in: float
    x2_in: float
    y2_in: float
    line_width_pt: float = 0.5


@dataclass(frozen=True)
class RectangleElement:
    x_in: float
    y_in: float
    width_in: float
    height_in: float
    line_width_pt: float = 0.5
