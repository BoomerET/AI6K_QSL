from dataclasses import dataclass, field
from typing import Union

from .elements import LineElement, RectangleElement, TextElement

CardElement = Union[TextElement, LineElement, RectangleElement]


@dataclass
class Card:
    width_in: float = 3.5
    height_in: float = 5.5
    elements: list[CardElement] = field(default_factory=list)

    def add(self, element: CardElement) -> CardElement:
        self.elements.append(element)
        return element
