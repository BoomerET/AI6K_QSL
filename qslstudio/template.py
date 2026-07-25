from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .card import Card
from .elements import LineElement, RectangleElement, TextElement


@dataclass(frozen=True)
class TemplateContext:
    values: dict[str, Any]

    def render(self, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        rendered = value
        for key, replacement in self.values.items():
            rendered = rendered.replace(f"{{{{ {key} }}}}", str(replacement))
            rendered = rendered.replace(f"{{{{{key}}}}}", str(replacement))
        return rendered


def _require_float(data: dict[str, Any], key: str) -> float:
    if key not in data:
        raise ValueError(f"Missing required template field: {key}")
    return float(data[key])


def load_card_template(path: Path, context: TemplateContext | None = None) -> Card:
    context = context or TemplateContext({})
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    card_data = data.get("card", {})
    card = Card(
        width_in=float(card_data.get("width_in", 3.5)),
        height_in=float(card_data.get("height_in", 5.5)),
    )

    for index, raw in enumerate(data.get("elements", []), start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"Element {index} must be a mapping.")

        element_type = raw.get("type")

        if element_type == "text":
            card.add(
                TextElement(
                    text=str(context.render(raw.get("value", ""))),
                    x_in=_require_float(raw, "x_in"),
                    y_in=_require_float(raw, "y_in"),
                    font_name=str(raw.get("font_name", "Helvetica")),
                    font_size=float(raw.get("font_size", 12)),
                    align=str(raw.get("align", "left")),
                )
            )

        elif element_type == "line":
            card.add(
                LineElement(
                    x1_in=_require_float(raw, "x1_in"),
                    y1_in=_require_float(raw, "y1_in"),
                    x2_in=_require_float(raw, "x2_in"),
                    y2_in=_require_float(raw, "y2_in"),
                    line_width_pt=float(raw.get("line_width_pt", 0.5)),
                )
            )

        elif element_type == "rectangle":
            card.add(
                RectangleElement(
                    x_in=_require_float(raw, "x_in"),
                    y_in=_require_float(raw, "y_in"),
                    width_in=_require_float(raw, "width_in"),
                    height_in=_require_float(raw, "height_in"),
                    line_width_pt=float(raw.get("line_width_pt", 0.5)),
                )
            )

        else:
            raise ValueError(
                f"Element {index} has unsupported type: {element_type!r}"
            )

    return card
