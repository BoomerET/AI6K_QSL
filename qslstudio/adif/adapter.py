from __future__ import annotations

from ..models import QSO


def qso_from_adif(record: dict[str, str]) -> QSO:
    """Convert one parsed ADIF record into the renderer's QSO model."""
    callsign = record.get("CALL", "").strip()

    if not callsign:
        raise ValueError("ADIF record is missing the CALL field")

    return QSO(
        contacted_callsign=callsign,
        date=_format_date(record.get("QSO_DATE", "")),
        time_utc=_format_time(record.get("TIME_ON", "")),
        frequency=_get_frequency(record),
        mode=record.get("MODE", "").strip(),
        rst_sent=record.get("RST_SENT", "").strip(),
        rst_received=record.get("RST_RCVD", "").strip(),
        remarks=record.get("COMMENT", "").strip(),
        qsl_message=record.get("QSLMSG", "").strip() or "TNX QSO",
    )


def _format_date(value: str) -> str:
    """Convert YYYYMMDD into YYYY-MM-DD."""
    value = value.strip()

    if len(value) == 8 and value.isdigit():
        return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"

    return value


def _format_time(value: str) -> str:
    """Convert HHMM or HHMMSS into HH:MM UTC."""
    value = value.strip()

    if len(value) >= 4 and value[:4].isdigit():
        return f"{value[0:2]}:{value[2:4]}"

    return value


def _get_frequency(record: dict[str, str]) -> str:
    """Use the exact frequency when present, otherwise fall back to band."""
    frequency = record.get("FREQ", "").strip()

    if frequency:
        return f"{frequency} MHz"

    return record.get("BAND", "").strip()
