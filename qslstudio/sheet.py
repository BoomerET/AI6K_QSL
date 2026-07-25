from dataclasses import dataclass, field
from pathlib import Path

from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from .card import Card
from .elements import LineElement, RectangleElement, TextElement
from .layout import Cardstock, PrinterCalibration


@dataclass
class Sheet:
    cardstock: Cardstock
    printer: PrinterCalibration
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        maximum = self.cardstock.columns * self.cardstock.rows
        if len(self.cards) >= maximum:
            raise ValueError(f"This sheet supports only {maximum} cards.")
        self.cards.append(card)

    def _panel_origin(self, index: int) -> tuple[float, float]:
        col = index % self.cardstock.columns
        row = index // self.cardstock.columns

        x_in = self.cardstock.origin_x_in + col * self.cardstock.card_width_in
        y_in = self.cardstock.origin_y_in + row * self.cardstock.card_height_in
        return x_in, y_in

    @staticmethod
    def _pdf_y(page_height_pt: float, top_origin_y_in: float) -> float:
        return page_height_pt - top_origin_y_in * inch

    def _begin_rotated_card(
        self,
        canvas: Canvas,
        page_height_pt: float,
        panel_x_in: float,
        panel_y_in: float,
    ) -> None:
        """
        Rotate a logical 5.5 x 3.5 landscape card clockwise into a physical
        3.5 x 5.5 perforated panel.

        After this transform, drawing coordinates are:
          x: 0..5.5 inches, left to right across the finished card
          y: 0..3.5 inches, top to bottom across the finished card
        """
        panel_left_pt = panel_x_in * inch
        panel_top_pt = self._pdf_y(page_height_pt, panel_y_in)

        canvas.saveState()
        canvas.translate(panel_left_pt, panel_top_pt)
        canvas.rotate(-90)
        canvas.scale(1, -1)

    def _draw_text(self, canvas: Canvas, element: TextElement) -> None:
        x_pt = element.x_in * inch
        y_pt = element.y_in * inch

        canvas.setFont(element.font_name, element.font_size)

        if element.align == "center":
            canvas.drawCentredString(x_pt, y_pt, element.text)
        elif element.align == "right":
            canvas.drawRightString(x_pt, y_pt, element.text)
        else:
            canvas.drawString(x_pt, y_pt, element.text)

    def _draw_line(self, canvas: Canvas, element: LineElement) -> None:
        canvas.setLineWidth(element.line_width_pt)
        canvas.line(
            element.x1_in * inch,
            element.y1_in * inch,
            element.x2_in * inch,
            element.y2_in * inch,
        )

    def _draw_rectangle(self, canvas: Canvas, element: RectangleElement) -> None:
        canvas.setLineWidth(element.line_width_pt)
        canvas.rect(
            element.x_in * inch,
            element.y_in * inch,
            element.width_in * inch,
            element.height_in * inch,
            stroke=1,
            fill=0,
        )

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

        for index, card in enumerate(self.cards):
            panel_x_in, panel_y_in = self._panel_origin(index)
            self._begin_rotated_card(
                canvas,
                page_height_pt,
                panel_x_in,
                panel_y_in,
            )

            for element in card.elements:
                if isinstance(element, TextElement):
                    self._draw_text(canvas, element)
                elif isinstance(element, LineElement):
                    self._draw_line(canvas, element)
                elif isinstance(element, RectangleElement):
                    self._draw_rectangle(canvas, element)
                else:
                    raise TypeError(f"Unsupported card element: {type(element)!r}")

            canvas.restoreState()

        canvas.restoreState()
        canvas.showPage()
        canvas.save()
        return output_path
