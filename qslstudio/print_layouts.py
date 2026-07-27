from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence

from .back import CARDSTOCK_CONFIG, PRINTER_CONFIG, TEMPLATE
from .layout import Cardstock, PrinterCalibration
from .models import QSO, StationProfile
from .sheet import Sheet
from .template import TemplateContext, load_card_template


class PrintLayout(Protocol):
    layout_id: str
    name: str
    description: str
    download_filename: str

    def render(
        self,
        qsos: Sequence[QSO],
        profile: StationProfile,
        output_path: Path,
    ) -> Path:
        ...


@dataclass(frozen=True, slots=True)
class ConfiguredCardstockLayout:
    layout_id: str = "configured-cardstock"
    name: str = "Configured cardstock"
    description: str = (
        "Uses the cardstock and printer calibration currently configured "
        "for AI6K QSL Studio."
    )
    download_filename: str = "QSL-cards.pdf"

    def render(
        self,
        qsos: Sequence[QSO],
        profile: StationProfile,
        output_path: Path,
    ) -> Path:
        if not qsos:
            raise ValueError("At least one QSO is required.")

        stock = Cardstock.load(CARDSTOCK_CONFIG)
        printer = PrinterCalibration.load(PRINTER_CONFIG)
        sheet = Sheet(stock, printer)

        for qso in qsos:
            values = {}
            values.update(profile.to_template_values())
            values.update(qso.to_template_values())

            sheet.add_card(
                load_card_template(
                    TEMPLATE,
                    TemplateContext(values),
                )
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return sheet.export_pdf(output_path)


DEFAULT_LAYOUT_ID = "configured-cardstock"

PRINT_LAYOUTS: dict[str, PrintLayout] = {
    DEFAULT_LAYOUT_ID: ConfiguredCardstockLayout(),
}


def get_print_layout(layout_id: str) -> PrintLayout:
    try:
        return PRINT_LAYOUTS[layout_id]
    except KeyError:
        raise KeyError(f"Unknown print layout: {layout_id}") from None


def list_print_layouts() -> tuple[PrintLayout, ...]:
    return tuple(PRINT_LAYOUTS.values())
