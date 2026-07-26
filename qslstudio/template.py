from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .card import Card
from .components import ComponentContext, build_qso_table, build_station_signature
from .elements import ImageElement, LineElement, RectangleElement, TextElement


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


def _resolve_asset_path(template_path: Path, value: str) -> str:
    asset_path = Path(value).expanduser()
    if asset_path.is_absolute():
        return str(asset_path)
    return str((template_path.parent / asset_path).resolve())


def load_card_template(
    path: Path,
    context: TemplateContext | None = None,
) -> Card:
    path = Path(path).resolve()
    context = context or TemplateContext({})
    component_context = ComponentContext(context.values)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    card_data = data.get("card", {})
    card = Card(
        width_in=float(card_data.get("width_in", 5.5)),
        height_in=float(card_data.get("height_in", 3.5)),
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

        elif element_type == "image":
            if "file" not in raw:
                raise ValueError(f"Image element {index} is missing 'file'.")

            rendered_file = str(context.render(raw["file"]))

            card.add(
                ImageElement(
                    file=_resolve_asset_path(path, rendered_file),
                    x_in=_require_float(raw, "x_in"),
                    y_in=_require_float(raw, "y_in"),
                    width_in=_require_float(raw, "width_in"),
                    height_in=_require_float(raw, "height_in"),
                    preserve_aspect_ratio=bool(
                        raw.get("preserve_aspect_ratio", True)
                    ),
                )
            )

        elif element_type == "qso_table":
            for element in build_qso_table(
                x_in=_require_float(raw, "x_in"),
                y_in=_require_float(raw, "y_in"),
                width_in=_require_float(raw, "width_in"),
                context=component_context,
            ):
                card.add(element)

        elif element_type == "station_signature":
            for element in build_station_signature(
                x_in=_require_float(raw, "x_in"),
                y_in=_require_float(raw, "y_in"),
                width_in=_require_float(raw, "width_in"),
                align=str(raw.get("align", "right")),
                context=component_context,
            ):
                card.add(element)

        else:
            raise ValueError(
                f"Element {index} has unsupported type: {element_type!r}"
            )

    return card
