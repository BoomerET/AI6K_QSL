from __future__ import annotations

import re


_TAG_PATTERN = re.compile(
    r"<([A-Za-z0-9_]+)(?::(\d+)(?::[^>]*)?)?>",
    re.IGNORECASE,
)


def parse_adif(text: str) -> list[dict[str, str]]:
    """Parse ADIF text into a list of QSO record dictionaries.

    Field names are normalized to uppercase.

    Example:
        <CALL:6>KE7NCO<BAND:3>40m<EOR>

    Becomes:
        {
            "CALL": "KE7NCO",
            "BAND": "40m",
        }
    """
    records: list[dict[str, str]] = []
    current_record: dict[str, str] = {}

    position = 0
    in_header = True

    while True:
        match = _TAG_PATTERN.search(text, position)

        if match is None:
            break

        field_name = match.group(1).upper()
        field_length_text = match.group(2)

        position = match.end()

        if field_name == "EOH":
            in_header = False
            current_record = {}
            continue

        if field_name == "EOR":
            if current_record:
                records.append(current_record)
                current_record = {}
            continue

        if field_length_text is None:
            continue

        field_length = int(field_length_text)
        field_value = text[position : position + field_length]
        position += field_length

        if not in_header:
            current_record[field_name] = field_value

    return records
