from dataclasses import dataclass
from typing import Any

from .elements import LineElement, TextElement


@dataclass(frozen=True)
class ComponentContext:
    values: dict[str, Any]

    def value(self, key: str, default: str = "") -> str:
        return str(self.values.get(key, default))


def build_qso_table(
    *,
    x_in: float,
    y_in: float,
    width_in: float,
    context: ComponentContext,
) -> list[object]:
    """
    Build a compact single-row QSO table.

    Coordinates use the logical 5.5 x 3.5-inch landscape card system.
    """
    column_ratios = {
        "date": 0.22,
        "utc": 0.13,
        "frequency": 0.25,
        "mode": 0.16,
        "rst": 0.12,
        "qsl": 0.12,
    }

    headers = [
        ("DATE", "date"),
        ("UTC", "utc"),
        ("FREQUENCY", "frequency"),
        ("MODE", "mode"),
        ("RST", "rst"),
        ("QSL", "qsl"),
    ]

    row_height = 0.31
    header_baseline = y_in + 0.14
    value_baseline = y_in + 0.46

    elements: list[object] = [
        LineElement(
            x1_in=x_in,
            y1_in=y_in + 0.23,
            x2_in=x_in + width_in,
            y2_in=y_in + 0.23,
            line_width_pt=0.45,
        ),
        LineElement(
            x1_in=x_in,
            y1_in=y_in + 0.57,
            x2_in=x_in + width_in,
            y2_in=y_in + 0.57,
            line_width_pt=0.45,
        ),
    ]

    current_x = x_in

    field_values = {
        "date": context.value("date"),
        "utc": context.value("time_utc"),
        "frequency": context.value("frequency"),
        "mode": context.value("mode"),
        "rst": context.value("rst_sent"),
        "qsl": context.value("qsl_message", "TNX"),
    }

    for header, key in headers:
        column_width = width_in * column_ratios[key]
        center_x = current_x + column_width / 2

        elements.extend(
            [
                TextElement(
                    text=header,
                    x_in=center_x,
                    y_in=header_baseline,
                    font_name="Helvetica-Bold",
                    font_size=7.0,
                    align="center",
                ),
                TextElement(
                    text=field_values[key],
                    x_in=center_x,
                    y_in=value_baseline,
                    font_name="Helvetica",
                    font_size=8.0,
                    align="center",
                ),
            ]
        )

        current_x += column_width

        if key != "qsl":
            elements.append(
                LineElement(
                    x1_in=current_x,
                    y1_in=y_in,
                    x2_in=current_x,
                    y2_in=y_in + row_height + 0.26,
                    line_width_pt=0.25,
                )
            )

    return elements


def build_station_signature(
    *,
    x_in: float,
    y_in: float,
    width_in: float,
    context: ComponentContext,
    align: str = "right",
) -> list[object]:
    if align not in {"left", "center", "right"}:
        raise ValueError(f"Unsupported station_signature alignment: {align}")

    anchor_x = {
        "left": x_in,
        "center": x_in + width_in / 2,
        "right": x_in + width_in,
    }[align]

    name = context.value("name")
    location = context.value("location")
    rig = context.value("rig")
    power = context.value("power")

    return [
        TextElement(
            text=f"{name} — {location}",
            x_in=anchor_x,
            y_in=y_in,
            font_name="Helvetica",
            font_size=8.0,
            align=align,
        ),
        TextElement(
            text=f"{rig} • {power}",
            x_in=anchor_x,
            y_in=y_in + 0.25,
            font_name="Helvetica",
            font_size=8.0,
            align=align,
        ),
    ]
