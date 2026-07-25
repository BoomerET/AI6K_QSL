from pathlib import Path

from qslstudio.elements import ImageElement
from qslstudio.template import load_card_template


def test_image_element_loads(tmp_path: Path) -> None:
    template = tmp_path / "image.yaml"
    template.write_text(
        """
card:
  width_in: 5.5
  height_in: 3.5
elements:
  - type: image
    file: assets/test.svg
    x_in: 1.0
    y_in: 1.2
    width_in: 2.0
    height_in: 1.0
""".strip(),
        encoding="utf-8",
    )

    card = load_card_template(template)

    assert len(card.elements) == 1
    element = card.elements[0]
    assert isinstance(element, ImageElement)
    assert element.file == "assets/test.svg"
    assert element.width_in == 2.0
