from pathlib import Path
from .adif import parse_adif, qso_from_adif
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig


def main() -> None:
    cfg = WavelogConfig.load(Path("config/config.yaml"))
    client = WavelogClient(cfg)

    print(f"Connecting to {cfg.url} ...")

    try:
        print(f"Version: {client.get_version()}")

        print("\nDownloading ADIF...")

        export = client.export_adif(station_id=1)

        print(f"Exported QSOs: {export.exported_qsos}")
        print(f"Last fetched ID: {export.last_fetched_id}")

        records = parse_adif(export.adif)

        print(f"Parsed QSOs: {len(records)}")

        if records:
            first_record = records[0]

            print("\nFirst parsed QSO:")
            print(f"  Call: {first_record.get('CALL', '')}")
            print(f"  Date: {first_record.get('QSO_DATE', '')}")
            print(f"  Time: {first_record.get('TIME_ON', '')}")
            print(f"  Band: {first_record.get('BAND', '')}")
            print(f"  Mode: {first_record.get('MODE', '')}")
            print(f"  RST sent: {first_record.get('RST_SENT', '')}")

            qso = qso_from_adif(first_record)

            print("\nMapped QSO:")
            print(f"  Callsign: {qso.contacted_callsign}")
            print(f"  Date: {qso.date}")
            print(f"  Time UTC: {qso.time_utc}")
            print(f"  Frequency: {qso.frequency}")
            print(f"  Mode: {qso.mode}")
            print(f"  RST sent: {qso.rst_sent}")
            print(f"  RST received: {qso.rst_received}")
            print(f"  Remarks: {qso.remarks}")
            print(f"  QSL message: {qso.qsl_message}")

        print("\nStations:")

        for station in client.get_station_profiles():
            print(f"  {station}")

        print("\nSUCCESS")

    except Exception as ex:
        print(f"FAILED: {ex}")


if __name__ == "__main__":
    main()
