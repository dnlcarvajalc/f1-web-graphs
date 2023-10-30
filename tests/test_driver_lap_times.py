import pandas as pd
import matplotlib.pyplot as plt
import src.variables as variables
import src.driver_lap_times as driver_lap_times
from unittest.mock import patch


@patch("src.utils.get_number_of_laps_done")
def test_main(mock_get_number_of_laps_done):
    mock_get_number_of_laps_done.return_value = 42  # Replace 42 with your desired value

    driver_lap_times.main(
        2022, 1, {"driver1": {"name": "perez", "color": "b", "alias": "ChequitoBB"}}
    )

    assert mock_get_number_of_laps_done.called_with(2022, 1, variables.BASE_URL)


@patch("src.utils.return_data_response")
def test_get_laptimes_dataframe(mock_return_data_response):
    sample_data = {
        "MRData": {
            "RaceTable": {
                "Race": {
                    "LapsList": {
                        "Lap": {
                            "Timing": [
                                {"@driverId": "perez", "@lap": "1", "@time": "1:30.123"},
                                {"@driverId": "max_verstappen", "@lap": "1", "@time": "1:31.456"},
                            ]
                        }
                    }
                }
            }
        }
    }
    mock_return_data_response.return_value = sample_data

    number_of_laps = 1
    year_race = 2022
    round_race = 1

    result_df = driver_lap_times.get_laptimes_dataframe(number_of_laps, year_race, round_race)

    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2  # Number of laps * number of drivers in sample_data


def test_plot_single_driver():
    data = {
        "@driverId": ["driver1", "driver2", "driver1", "driver2"],
        "@lap": [1, 1, 2, 2],
        "@time": [1.23, 1.45, 2.34, 2.56],
    }
    full_df = pd.DataFrame(data)

    driver_name = "driver1"
    color_plot = "b"
    label_driver = "Driver 1"

    driver_lap_times.plot_single_driver(full_df, driver_name, color_plot, label_driver)

    lines = plt.gca().get_lines()
    assert len(lines) == 1
    assert lines[0].get_color() == color_plot
    assert lines[0].get_label() == label_driver
    assert lines[0].get_marker() == "."

    x_values = lines[0].get_xdata()
    assert x_values.tolist() == [1, 2]

    y_values = lines[0].get_ydata()
    assert y_values.tolist() == [1.23, 2.34]

    plt.close()


@patch("src.driver_lap_times.plot_single_driver")
@patch("matplotlib.pyplot.figure")
@patch("matplotlib.pyplot.xlabel")
@patch("matplotlib.pyplot.ylabel")
@patch("matplotlib.pyplot.title")
@patch("matplotlib.pyplot.legend")
@patch("matplotlib.pyplot.xticks")
@patch("matplotlib.pyplot.grid")
@patch("matplotlib.pyplot.show")
def test_plot_graph(
    mock_show,
    mock_grid,
    mock_xticks,
    mock_legend,
    mock_title,
    mock_ylabel,
    mock_xlabel,
    mock_figure,
    mock_plot_single_driver,
):
    all_laps_df = pd.DataFrame(
        {
            "@driverId": ["driver1", "driver2", "driver1", "driver2"],
            "@lap": [1, 1, 2, 2],
            "@time": [1.23, 1.45, 2.34, 2.56],
        }
    )
    driver_list = {
        "driver1": {"name": "Driver 1", "color": "b", "alias": "D1"},
        "driver2": {"name": "Driver 2", "color": "g", "alias": "D2"},
    }
    number_of_laps = 10
    driver_lap_times.plot_graph(all_laps_df, driver_list, number_of_laps)

    assert mock_figure.called
    assert mock_xlabel.called_with("Laps")
    assert mock_ylabel.called_with("Lap Time (seconds)")
    assert mock_title.called_with("Lap Times vs. Laps")
    assert mock_legend.called
    assert mock_xticks.called_with(range(0, number_of_laps, 2))
    assert mock_grid.called
    assert mock_show.called

    assert mock_plot_single_driver.call_count == len(driver_list)
