import pandas as pd
import matplotlib.pyplot as plt
import src.utils as utils
import src.variables as variables


def main(year_race: int, round_race: int, driver_list: dict) -> None:
    """constructor of the class responsible to create the laptime chart.

    Args:
        year_race (int): year of the race.
        round_race (int): number of the race in the f1 calendar.
        driver_list (dict): dictionary with driver information that is wanted to be in chart.
    """
    number_of_laps = utils.get_number_of_laps_done(year_race, round_race, variables.BASE_URL)
    all_laps_df = get_laptimes_dataframe(number_of_laps, year_race, round_race)
    plot_graph(all_laps_df, driver_list, number_of_laps)


def get_laptimes_dataframe(number_of_laps: int, year_race: int, round_race: int) -> pd.DataFrame:
    """This function does the extraction of all lap times from the specific race.

    Args:
        number_of_laps (int): number of laps done for the driver who finished first.
        year_race (int): year of the race.
        round_race (int): number of the race in the current year.

    Returns:
        pd.DataFrame: dataframe with all info of drivers and laptimes.
    """
    all_laps_df = pd.DataFrame()
    for lap_number in range(1, int(number_of_laps) + 1):
        endpoint = f"{year_race}/{round_race}/laps/{lap_number}"
        url = variables.BASE_URL + endpoint
        data_dict = utils.return_data_response(url)

        timing_data = data_dict["MRData"]["RaceTable"]["Race"]["LapsList"]["Lap"]["Timing"]
        one_lap_df = pd.DataFrame(timing_data)
        all_laps_df = pd.concat([all_laps_df, one_lap_df], axis=0)

    all_laps_df = utils.laptimes_to_seconds(all_laps_df)

    return all_laps_df


def plot_single_driver(
    full_df: pd.DataFrame,
    driver_name: str,
    color_plot: str,
    label_driver: str,
) -> None:
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


def plot_graph(all_laps_df: pd.DataFrame, driver_list: list, number_of_laps: int) -> None:
    """orchestate the chart
    Args:
        all_laps_df (pd.DataFrame): dataframe with all information
        driver_list (list): list with drivers to plot
        number_of_laps (int): total of number of laps made in the race
    """
    plt.figure(figsize=(10, 6))
    for driver in driver_list:
        plot_single_driver(
            all_laps_df,
            driver_list[driver]["name"],
            driver_list[driver]["color"],
            driver_list[driver]["alias"],
        )
    plt.xlabel("Laps")
    plt.ylabel("Lap Time (seconds)")
    plt.title("Lap Times vs. Laps")
    plt.legend()
    plt.xticks(range(0, int(number_of_laps), 2))  # Display every 2nd label
    plt.grid(True)
    plt.show()
