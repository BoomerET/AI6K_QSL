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
        printer_config: Path = PRINTER_CONFIG,
    ) -> Path:
        ...


@dataclass(frozen=True, slots=True)
class LetterFourUpLayout:
    # Four 5.5 x 3.5 inch QSL cards on US Letter paper.

    layout_id: str = "letter-4up"
    name: str = "US Letter — 4-up"
    description: str = (
        "Prints four landscape 5.5 × 3.5 inch QSL cards on each "
        "8.5 × 11 inch sheet, leaving a 1.5 inch strip."
    )
    download_filename: str = "QSL-cards-letter-4up.pdf"

    def render(
        self,
        qsos: Sequence[QSO],
        profile: StationProfile,
        output_path: Path,
        printer_config: Path = PRINTER_CONFIG,
    ) -> Path:
        if not qsos:
            raise ValueError("At least one QSO is required.")

        stock = Cardstock(
            paper_width_in=8.5,
            paper_height_in=11.0,
            card_width_in=3.5,
            card_height_in=5.5,
            columns=2,
            rows=2,
            origin_x_in=0.0,
            origin_y_in=0.0,
            strip_width_in=1.5,
        )
        printer = PrinterCalibration.load(printer_config)
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
        printer_config: Path = PRINTER_CONFIG,
    ) -> Path:
        if not qsos:
            raise ValueError("At least one QSO is required.")

        stock = Cardstock.load(CARDSTOCK_CONFIG)
        printer = PrinterCalibration.load(printer_config)
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
    "letter-4up": LetterFourUpLayout(),
}


def get_print_layout(layout_id: str) -> PrintLayout:
    try:
        return PRINT_LAYOUTS[layout_id]
    except KeyError:
        raise KeyError(f"Unknown print layout: {layout_id}") from None


def list_print_layouts() -> tuple[PrintLayout, ...]:
    return tuple(PRINT_LAYOUTS.values())
