from dataclasses import dataclass, field
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg

from .card import Card
from .elements import (
    ImageElement,
    LineElement,
    RectangleElement,
    TextElement,
)
from .layout import Cardstock, PrinterCalibration


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Sheet:
    cardstock: Cardstock
    printer: PrinterCalibration
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def cards_per_page(self) -> int:
        return self.cardstock.columns * self.cardstock.rows

    def _panel_origin(self, index: int) -> tuple[float, float]:
        col = index % self.cardstock.columns
        row = index // self.cardstock.columns
        return (
            self.cardstock.origin_x_in + col * self.cardstock.card_width_in,
            self.cardstock.origin_y_in + row * self.cardstock.card_height_in,
        )

    def _map_point(
        self,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
        x_in: float,
        y_in: float,
    ) -> tuple[float, float]:
        physical_x_in = panel_x_in + self.cardstock.card_width_in - y_in
        physical_y_from_top_in = panel_y_in + x_in

        return (
            physical_x_in * inch,
            page_height_pt - physical_y_from_top_in * inch,
        )

    def _draw_text(
        self,
        canvas: Canvas,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
        element: TextElement,
    ) -> None:
        x_pt, y_pt = self._map_point(
            page_height_pt,
            panel_x_in,
            panel_y_in,
            element.x_in,
            element.y_in,
        )

        canvas.saveState()
        canvas.translate(x_pt, y_pt)
        canvas.rotate(-90)
        canvas.setFont(element.font_name, element.font_size)

        if element.align == "center":
            canvas.drawCentredString(0, 0, element.text)
        elif element.align == "right":
            canvas.drawRightString(0, 0, element.text)
        else:
            canvas.drawString(0, 0, element.text)

        canvas.restoreState()

    def _draw_line(
        self,
        canvas: Canvas,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
        element: LineElement,
    ) -> None:
        x1, y1 = self._map_point(
            page_height_pt, panel_x_in, panel_y_in,
            element.x1_in, element.y1_in,
        )
        x2, y2 = self._map_point(
            page_height_pt, panel_x_in, panel_y_in,
            element.x2_in, element.y2_in,
        )

        canvas.setLineWidth(element.line_width_pt)
        canvas.line(x1, y1, x2, y2)

    def _draw_rectangle(
        self,
        canvas: Canvas,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
        element: RectangleElement,
    ) -> None:
        corners = [
            (element.x_in, element.y_in),
            (element.x_in + element.width_in, element.y_in),
            (
                element.x_in + element.width_in,
                element.y_in + element.height_in,
            ),
            (element.x_in, element.y_in + element.height_in),
        ]

        mapped = [
            self._map_point(
                page_height_pt,
                panel_x_in,
                panel_y_in,
                x,
                y,
            )
            for x, y in corners
        ]

        path = canvas.beginPath()
        path.moveTo(*mapped[0])
        for point in mapped[1:]:
            path.lineTo(*point)
        path.close()

        canvas.setLineWidth(element.line_width_pt)
        canvas.drawPath(path, stroke=1, fill=0)

    def _resolve_asset(self, filename: str) -> Path:
        candidate = Path(filename)
        if candidate.is_absolute():
            path = candidate
        else:
            path = ROOT / filename

        if not path.exists():
            raise FileNotFoundError(f"Image asset not found: {path}")
        return path

    def _draw_image(
        self,
        canvas: Canvas,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
        element: ImageElement,
    ) -> None:
        asset = self._resolve_asset(element.file)

        # Anchor at logical top-left, then rotate the image into the panel.
        x_pt, y_pt = self._map_point(
            page_height_pt,
            panel_x_in,
            panel_y_in,
            element.x_in,
            element.y_in + element.height_in,
        )

        width_pt = element.width_in * inch
        height_pt = element.height_in * inch

        canvas.saveState()
        canvas.translate(x_pt, y_pt)
        canvas.rotate(-90)

        suffix = asset.suffix.lower()

        if suffix == ".svg":
            drawing = svg2rlg(str(asset))
            if drawing is None:
                raise ValueError(f"Unable to load SVG: {asset}")

            scale_x = width_pt / drawing.width
            scale_y = height_pt / drawing.height

            if element.preserve_aspect_ratio:
                scale = min(scale_x, scale_y)
                draw_width = drawing.width * scale
                draw_height = drawing.height * scale
                offset_x = (width_pt - draw_width) / 2
                offset_y = (height_pt - draw_height) / 2
                canvas.translate(offset_x, offset_y)
                canvas.scale(scale, scale)
            else:
                canvas.scale(scale_x, scale_y)

            renderPDF.draw(drawing, canvas, 0, 0)

        elif suffix in {".png", ".jpg", ".jpeg"}:
            canvas.drawImage(
                str(asset),
                0,
                0,
                width=width_pt,
                height=height_pt,
                preserveAspectRatio=element.preserve_aspect_ratio,
                mask="auto",
            )

        else:
            raise ValueError(
                f"Unsupported image format {suffix!r}: {asset}"
            )

        canvas.restoreState()

    def export_pdf(self, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        page_width_pt = self.cardstock.paper_width_in * inch
        page_height_pt = self.cardstock.paper_height_in * inch

        canvas = Canvas(
            str(output_path),
            pagesize=(page_width_pt, page_height_pt),
        )

        canvas.saveState()
        canvas.translate(
            self.printer.x_offset_in * inch,
            -self.printer.y_offset_in * inch,
        )
        canvas.scale(self.printer.x_scale, self.printer.y_scale)

        cards_per_page = self.cards_per_page

        for index, card in enumerate(self.cards):
            page_index = index // cards_per_page
            panel_index = index % cards_per_page

            if panel_index == 0 and page_index > 0:
                canvas.restoreState()
                canvas.showPage()
                canvas.saveState()
                canvas.translate(
                    self.printer.x_offset_in * inch,
                    -self.printer.y_offset_in * inch,
                )
                canvas.scale(
                    self.printer.x_scale,
                    self.printer.y_scale,
                )

            panel_x_in, panel_y_in = self._panel_origin(panel_index)

            for element in card.elements:
                if isinstance(element, TextElement):
                    self._draw_text(
                        canvas, page_height_pt,
                        panel_x_in, panel_y_in, element,
                    )
                elif isinstance(element, LineElement):
                    self._draw_line(
                        canvas, page_height_pt,
                        panel_x_in, panel_y_in, element,
                    )
                elif isinstance(element, RectangleElement):
                    self._draw_rectangle(
                        canvas, page_height_pt,
                        panel_x_in, panel_y_in, element,
                    )
                elif isinstance(element, ImageElement):
                    self._draw_image(
                        canvas, page_height_pt,
                        panel_x_in, panel_y_in, element,
                    )
                else:
                    raise TypeError(
                        f"Unsupported card element: {type(element)!r}"
                    )

        canvas.restoreState()
        canvas.showPage()
        canvas.save()
        return output_path
