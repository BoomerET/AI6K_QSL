from qslstudio.components import (
    ComponentContext,
    build_qso_table,
    build_station_signature,
)
from qslstudio.elements import LineElement, TextElement


def test_qso_table_expands_to_drawing_elements() -> None:
    context = ComponentContext(
        {
            "date": "2026-07-25",
            "time_utc": "1915",
            "frequency": "14.074 MHz",
            "mode": "FT8",
            "rst_sent": "-08",
            "qsl_message": "TNX",
        }
    )

    elements = build_qso_table(
        x_in=0.35,
        y_in=1.12,
        width_in=4.80,
        context=context,
    )

    assert any(
        isinstance(element, TextElement) and element.text == "14.074 MHz"
        for element in elements
    )
    assert any(isinstance(element, LineElement) for element in elements)


def test_station_signature_uses_profile_values() -> None:
    context = ComponentContext(
        {
            "name": "David Berkompas",
            "location": "Prosper, Texas",
            "rig": "Icom IC-7300",
            "power": "100 W",
        }
    )

    elements = build_station_signature(
        x_in=2.65,
        y_in=2.70,
        width_in=2.50,
        align="right",
        context=context,
    )

    assert elements[0].text == "David Berkompas — Prosper, Texas"
    assert elements[1].text == "Icom IC-7300 • 100 W"
