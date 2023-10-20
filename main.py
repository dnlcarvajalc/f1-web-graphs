import driver_lap_times
from variables import year_race, round_race, drivers_for_lap_times

if __name__ == "__main__":
    driver_lap_times.plot_lap_times(
        year_race=year_race, round_race=round_race, driver_list=drivers_for_lap_times
    )
