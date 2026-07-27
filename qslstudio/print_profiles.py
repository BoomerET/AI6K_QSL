from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .print_layouts import get_print_layout

ROOT = Path(__file__).resolve().parents[1]
PRINT_PROFILES_CONFIG = ROOT / "config" / "print_profiles.yaml"


@dataclass(frozen=True, slots=True)
class PrintProfile:
    profile_id: str
    name: str
    description: str
    layout_id: str
    printer_config: Path
    download_filename: str | None = None

    @classmethod
    def from_mapping(cls, profile_id: str, data: dict[str, object]) -> "PrintProfile":
        printer_config = Path(str(data["printer_config"]))
        if not printer_config.is_absolute():
            printer_config = ROOT / printer_config

        return cls(
            profile_id=profile_id,
            name=str(data["name"]),
            description=str(data.get("description", "")),
            layout_id=str(data["layout_id"]),
            printer_config=printer_config,
            download_filename=(
                str(data["download_filename"])
                if data.get("download_filename")
                else None
            ),
        )

    @property
    def layout(self):
        return get_print_layout(self.layout_id)

    @property
    def effective_download_filename(self) -> str:
        return self.download_filename or self.layout.download_filename


def load_print_profiles(path: Path = PRINT_PROFILES_CONFIG) -> tuple[str, dict[str, PrintProfile]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    default_profile_id = str(data["default_profile"])
    raw_profiles = data.get("profiles", {})

    profiles = {
        profile_id: PrintProfile.from_mapping(profile_id, values)
        for profile_id, values in raw_profiles.items()
    }

    if default_profile_id not in profiles:
        raise ValueError(f"Default print profile {default_profile_id!r} is not defined.")

    for profile in profiles.values():
        get_print_layout(profile.layout_id)
        if not profile.printer_config.exists():
            raise FileNotFoundError(f"Printer calibration not found: {profile.printer_config}")

    return default_profile_id, profiles


def get_print_profile(profile_id: str) -> PrintProfile:
    _, profiles = load_print_profiles()
    try:
        return profiles[profile_id]
    except KeyError:
        raise KeyError(f"Unknown print profile: {profile_id}") from None


def list_print_profiles() -> tuple[PrintProfile, ...]:
    _, profiles = load_print_profiles()
    return tuple(profiles.values())


def get_default_print_profile_id() -> str:
    default_profile_id, _ = load_print_profiles()
    return default_profile_id
