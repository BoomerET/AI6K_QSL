from pathlib import Path
from pprint import pprint
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig


def main() -> None:
    cfg = WavelogConfig.load(Path("config/config.yaml"))
    client = WavelogClient(cfg)

    print("Connecting to", cfg.url, "...")

    try:
        print("Version:", client.get_version())
    
        print("\nDownloading ADIF...")
    
        export = client.export_adif(station_id=1)
    
        print(f"Exported QSOs: {export.exported_qsos}")
        print(f"Last fetched ID: {export.last_fetched_id}")
        print(export.adif[:500])
    
        print("\nStations:")
    
        for station in client.get_station_profiles():
            print(f"  {station}")
    
        print("\nSUCCESS")
    
    except Exception as ex:
        print(f"FAILED: {ex}")


if __name__ == "__main__":
    main()
