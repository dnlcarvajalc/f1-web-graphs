import requests
import xmltodict
import pandas as pd


def return_data_response(url: str) -> dict:
    """this function does an http get request to the url specified in the args and returns
    the info in a dictionary.

    Args:
        url (str): url of the api to do the request.

    Returns:
        dict: dictionary with info of the response.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = xmltodict.parse(response.content)
        return data_dict
    else:
        print("Request failed with status code:", response.status_code)


def get_number_of_laps_done(year_race: int, round_race: int, base_url: str) -> int:
    """this function gets a response using the function created above (return_data_response)
    and extracts the number of laps made by the driver who finished in the first position.

    Args:
        year_race (int): year of the race
        round_race (int): number of the race in the f1 calendar
        base_url (str): url of the api

    Returns:
        int: the number of laps made by the driver who finished in the first position.
    """
    endpoint = f"{year_race}/{round_race}/results"
    url = base_url + endpoint
    data_dict = return_data_response(url)
    print(data_dict)

    driver_results = data_dict["MRData"]["RaceTable"]["Race"]["ResultsList"]["Result"]
    for driver in driver_results:
        if driver["@position"] == "1":
            number_of_laps = driver["Laps"]
    return number_of_laps


def laptimes_to_seconds(dataframe: pd.DataFrame) -> pd.DataFrame:
    """converts the values of a dataframe with the column @time that have laptimes with
    minutes, seconds and microseconds to a seconds format.

    Args:
        dataframe (pd.DataFrame): dataframe of pandas with the ergast api response.

    Returns:
        pd.DataFrame: returns the same dataframe with seconds value in time column.
    """
    dataframe["@time"] = (
        pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.minute * 60
        + pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.second
        + pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.microsecond / 1000000
    )

    return dataframe
