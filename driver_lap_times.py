import pandas as pd
import matplotlib.pyplot as plt
import utils

BASE_URL = "https://ergast.com/api/f1/"


class plot_lap_times:
    def __init__(self, year_race: int, round_race: int, driver_list: dict) -> None:
        self.year_race, self.round_race, self.driver_list = (
            year_race,
            round_race,
            driver_list,
        )
        self.number_of_laps = utils.get_number_of_laps_done(
            self.year_race, self.round_race, BASE_URL
        )
        self.all_laps_df = self.get_laptimes_dataframe(self.number_of_laps)
        self.plot_graph()

    def get_laptimes_dataframe(self, number_of_laps: int):
        all_laps_df = pd.DataFrame()
        for lap_number in range(1, int(number_of_laps) + 1):
            endpoint = f"{self.year_race}/{self.round_race}/laps/{lap_number}"
            url = BASE_URL + endpoint
            data_dict = utils.return_data_response(url)

            timing_data = data_dict["MRData"]["RaceTable"]["Race"]["LapsList"]["Lap"]["Timing"]
            one_lap_df = pd.DataFrame(timing_data)
            all_laps_df = pd.concat([all_laps_df, one_lap_df], axis=0)

        # Convert lap times to seconds for plotting
        all_laps_df["@time"] = (
            pd.to_datetime(all_laps_df["@time"], format="%M:%S.%f").dt.minute * 60
            + pd.to_datetime(all_laps_df["@time"], format="%M:%S.%f").dt.second
            + pd.to_datetime(all_laps_df["@time"], format="%M:%S.%f").dt.microsecond
            / 1000000
        )

        return all_laps_df

    def plot_single_driver(
        self,
        full_df: pd.DataFrame,
        driver_name: str,
        color_plot: str,
        label_driver: str,
    ):
        driver_df_mask = full_df["@driverId"] == driver_name
        driver_df = pd.DataFrame()
        driver_df = full_df[driver_df_mask]
        plt.plot(
            driver_df["@lap"],
            driver_df["@time"],
            marker=".",
            linestyle="-",
            color=color_plot,
            label=label_driver,
        )

    def plot_graph(self):
        plt.figure(figsize=(10, 6))
        for driver in self.driver_list:
            self.plot_single_driver(
                self.all_laps_df,
                self.driver_list[driver]["name"],
                self.driver_list[driver]["color"],
                self.driver_list[driver]["alias"],
            )
        plt.xlabel("Laps")
        plt.ylabel("Lap Time (seconds)")
        plt.title("Lap Times vs. Laps")
        plt.legend()
        plt.xticks(range(0, int(self.number_of_laps), 2))  # Display every 2nd label
        plt.grid(True)
        plt.show()
