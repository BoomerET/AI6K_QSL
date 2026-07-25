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

    def _card_origin(self, index: int) -> tuple[float, float]:
        col = index % self.cardstock.columns
        row = index // self.cardstock.columns

        x_in = self.cardstock.origin_x_in + col * self.cardstock.card_width_in
        y_in = self.cardstock.origin_y_in + row * self.cardstock.card_height_in
        return x_in, y_in

    @staticmethod
    def _pdf_y(page_height_pt: float, top_origin_y_in: float) -> float:
        return page_height_pt - top_origin_y_in * inch

    def _draw_text(
        self,
        canvas: Canvas,
        page_height_pt: float,
        card_x_in: float,
        card_y_in: float,
        element: TextElement,
    ) -> None:
        x_pt = (card_x_in + element.x_in) * inch
        y_pt = self._pdf_y(page_height_pt, card_y_in + element.y_in)

        canvas.setFont(element.font_name, element.font_size)

        if element.align == "center":
            canvas.drawCentredString(x_pt, y_pt, element.text)
        elif element.align == "right":
            canvas.drawRightString(x_pt, y_pt, element.text)
        else:
            canvas.drawString(x_pt, y_pt, element.text)

    def _draw_line(
        self,
        canvas: Canvas,
        page_height_pt: float,
        card_x_in: float,
        card_y_in: float,
        element: LineElement,
    ) -> None:
        x1 = (card_x_in + element.x1_in) * inch
        y1 = self._pdf_y(page_height_pt, card_y_in + element.y1_in)
        x2 = (card_x_in + element.x2_in) * inch
        y2 = self._pdf_y(page_height_pt, card_y_in + element.y2_in)

        canvas.setLineWidth(element.line_width_pt)
        canvas.line(x1, y1, x2, y2)

    def _draw_rectangle(
        self,
        canvas: Canvas,
        page_height_pt: float,
        card_x_in: float,
        card_y_in: float,
        element: RectangleElement,
    ) -> None:
        x_pt = (card_x_in + element.x_in) * inch
        top_pt = self._pdf_y(page_height_pt, card_y_in + element.y_in)
        width_pt = element.width_in * inch
        height_pt = element.height_in * inch
        bottom_pt = top_pt - height_pt

        canvas.setLineWidth(element.line_width_pt)
        canvas.rect(x_pt, bottom_pt, width_pt, height_pt, stroke=1, fill=0)

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
            card_x_in, card_y_in = self._card_origin(index)

            for element in card.elements:
                if isinstance(element, TextElement):
                    self._draw_text(
                        canvas,
                        page_height_pt,
                        card_x_in,
                        card_y_in,
                        element,
                    )
                elif isinstance(element, LineElement):
                    self._draw_line(
                        canvas,
                        page_height_pt,
                        card_x_in,
                        card_y_in,
                        element,
                    )
                elif isinstance(element, RectangleElement):
                    self._draw_rectangle(
                        canvas,
                        page_height_pt,
                        card_x_in,
                        card_y_in,
                        element,
                    )
                else:
                    raise TypeError(f"Unsupported card element: {type(element)!r}")

        canvas.restoreState()
        canvas.showPage()
        canvas.save()
        return output_path
