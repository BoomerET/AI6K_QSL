from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrintLayout:
    layout_id: str
    name: str
    description: str
    download_filename: str


DEFAULT_LAYOUT_ID = "configured-cardstock"

PRINT_LAYOUTS = {
    DEFAULT_LAYOUT_ID: PrintLayout(
        layout_id=DEFAULT_LAYOUT_ID,
        name="Configured cardstock",
        description=(
            "Uses the cardstock and printer calibration currently configured "
            "for AI6K QSL Studio."
        ),
        download_filename="QSL-cards.pdf",
    ),
}


def get_print_layout(layout_id: str) -> PrintLayout:
    try:
        return PRINT_LAYOUTS[layout_id]
    except KeyError:
        raise KeyError(f"Unknown print layout: {layout_id}") from None
