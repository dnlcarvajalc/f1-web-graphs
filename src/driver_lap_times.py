import pandas as pd
import matplotlib.pyplot as plt
import src.utils as utils
from src.variables import BASE_URL


class plot_lap_times:
    def __init__(self, year_race: int, round_race: int, driver_list: dict) -> None:
        """constructor of the class responsible to create the laptime chart.

        Args:
            year_race (int): year of the race.
            round_race (int): number of the race in the f1 calendar.
            driver_list (dict): dictionary with driver information that is wanted to be in chart.
        """
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

    def get_laptimes_dataframe(self, number_of_laps: int) -> pd.DataFrame:
        """This function does the extraction of all lap times from the specific race.

        Args:
            number_of_laps (int): number of laps done for the driver who finished first.

        Returns:
            pd.DataFrame: dataframe with all info of drivers and laptimes.
        """
        all_laps_df = pd.DataFrame()
        for lap_number in range(1, int(number_of_laps) + 1):
            endpoint = f"{self.year_race}/{self.round_race}/laps/{lap_number}"
            url = BASE_URL + endpoint
            data_dict = utils.return_data_response(url)

            timing_data = data_dict["MRData"]["RaceTable"]["Race"]["LapsList"]["Lap"]["Timing"]
            one_lap_df = pd.DataFrame(timing_data)
            all_laps_df = pd.concat([all_laps_df, one_lap_df], axis=0)

        all_laps_df = utils.laptimes_to_seconds(all_laps_df)

        return all_laps_df

    def plot_single_driver(
        self,
        full_df: pd.DataFrame,
        driver_name: str,
        color_plot: str,
        label_driver: str,
    ):
        """plots driver by driver in the figure created before calling this function.

        Args:
            full_df (pd.DataFrame): dataframe with all the information.
            driver_name (str): driver to mask the dataframe with specific information.
            color_plot (str): color to be plotted
            label_driver (str): name to be plotted
        """
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
        """orchestate the chart"""
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
