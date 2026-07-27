from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import yaml


CONFIG_PATH = (
    Path.home()
    / ".config"
    / "ai6k-qsl-studio"
    / "config.yaml"
)


@dataclass
class WavelogConfig:
    url: str
    api_key: str

    def __post_init__(self) -> None:
        self.url = self.url.strip().rstrip("/")
        self.api_key = self.api_key.strip()

        if not self.url:
            raise ValueError("Wavelog URL is required.")

        if not self.api_key:
            raise ValueError("Wavelog API key is required.")

    @classmethod
    def load(cls, path: Path = CONFIG_PATH) -> "WavelogConfig":
        if not path.exists():
            raise FileNotFoundError(
                f"Wavelog configuration does not exist: {path}"
            )

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        wavelog = data.get("wavelog") or {}

        return cls(
            url=str(wavelog.get("url", "")),
            api_key=str(wavelog.get("api_key", "")),
        )

    @classmethod
    def load_effective(cls) -> "WavelogConfig":
        environment_url = os.getenv("WAVELOG_URL", "").strip()
        environment_api_key = os.getenv(
            "WAVELOG_API_KEY",
            "",
        ).strip()

        if environment_url or environment_api_key:
            stored: WavelogConfig | None = None

            if CONFIG_PATH.exists():
                try:
                    stored = cls.load(CONFIG_PATH)
                except Exception:
                    stored = None

            return cls(
                url=environment_url or (
                    stored.url if stored else ""
                ),
                api_key=environment_api_key or (
                    stored.api_key if stored else ""
                ),
            )

        return cls.load(CONFIG_PATH)

    @classmethod
    def is_configured(cls) -> bool:
        try:
            cls.load_effective()
        except (
            FileNotFoundError,
            KeyError,
            TypeError,
            ValueError,
            yaml.YAMLError,
        ):
            return False

        return True

    @classmethod
    def environment_override_active(cls) -> bool:
        return bool(
            os.getenv("WAVELOG_URL", "").strip()
            or os.getenv("WAVELOG_API_KEY", "").strip()
        )

    def save(self, path: Path = CONFIG_PATH) -> Path:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "wavelog": {
                "url": self.url,
                "api_key": self.api_key,
            }
        }

        temporary_path = path.with_suffix(".tmp")
        temporary_path.write_text(
            yaml.safe_dump(
                data,
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        temporary_path.chmod(0o600)
        temporary_path.replace(path)
        path.chmod(0o600)

        return path
