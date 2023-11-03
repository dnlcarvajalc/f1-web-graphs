import src.driver_lap_times as driver_lap_times
from src.variables import year_race, round_race, drivers_for_lap_times

if __name__ == "__main__":
    driver_lap_times.main(
        year_race=year_race, round_race=round_race, driver_list=drivers_for_lap_times
    )
