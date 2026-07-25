from pathlib import Path

from qslstudio.elements import TextElement
from qslstudio.template import TemplateContext, load_card_template


def test_template_substitution(tmp_path: Path) -> None:
    template = tmp_path / "front.yaml"
    template.write_text(
        """
card:
  width_in: 3.5
  height_in: 5.5
elements:
  - type: text
    value: "{{ callsign }}"
    x_in: 1.75
    y_in: 1.0
    align: center
""".strip(),
        encoding="utf-8",
    )

    card = load_card_template(
        template,
        TemplateContext({"callsign": "AI6K"}),
    )

    assert len(card.elements) == 1
    element = card.elements[0]
    assert isinstance(element, TextElement)
    assert element.text == "AI6K"
    assert element.x_in == 1.75
