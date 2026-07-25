from pathlib import Path
from .wavelog.client import WavelogClient
from .wavelog.config import WavelogConfig

def main():
    cfg=WavelogConfig.load(Path("config/config.yaml"))
    c=WavelogClient(cfg)
    print(f"Connecting to {cfg.url}")
    try:
        print("Version:",c.get_version())
        #print("Station:",c.get_station_profile())
        stations = c.get_station_profiles()

        print("\nStations:")

        for station in stations:
            active = " (active)" if station.active else ""
            print(
                f"  {station.station_id}: "
                f"{station.profile_name} "
                f"({station.callsign}){active}"
            )
        print("SUCCESS")
    except Exception as ex:
        print("FAILED:",ex)

if __name__=="__main__":
    main()
