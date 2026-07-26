from pathlib import Path

from .services import fetch_recent_qsos, generate_back_pdf


ROOT = Path(__file__).resolve().parents[1]
LIVE_OUTPUT = ROOT / "output" / "AI6K_QSL_live_back.pdf"


def generate(output_path: Path = LIVE_OUTPUT) -> Path:
    print("Downloading QSOs from Wavelog...")

    profile, qsos = fetch_recent_qsos(limit=4)

    print(f"Using station profile: {profile.callsign}")

    for qso in qsos:
        print(
            f"Rendering {qso.contacted_callsign} "
            f"from {qso.date} at {qso.time_utc} UTC..."
        )

    return generate_back_pdf(
        qsos=qsos,
        profile=profile,
        output_path=output_path,
    )


def main() -> None:
    output_path = generate()
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
