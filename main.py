import driver_lap_times

drivers_for_lap_times = {
    "driver1": {"name": "perez", "color": "b", "alias": "ChequitoBB"},
    "driver2": {"name": "max_verstappen", "color": "r", "alias": "Srto Maximiliano"},
    "driver3": {"name": "sainz", "color": "y", "alias": "Il Matador"},
    "driver4": {"name": "russell", "color": "g", "alias": "Mr Saturday"},
}

if __name__ == "__main__":
    driver_lap_times.plot_lap_times(
        year_race=2023, round_race=15, driver_list=drivers_for_lap_times
    )
