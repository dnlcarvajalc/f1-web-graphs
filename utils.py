import requests
import xmltodict
import pandas as pd


def return_data_response(url: str) -> dict:
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = xmltodict.parse(response.content)
        return data_dict
    else:
        print("Request failed with status code:", response.status_code)


def get_number_of_laps_done(year_race: int, round_race: int, base_url: str) -> int:
    endpoint = f"{year_race}/{round_race}/results"
    url = base_url + endpoint
    data_dict = return_data_response(url)

    driver_results = data_dict["MRData"]["RaceTable"]["Race"]["ResultsList"]["Result"]
    for driver in driver_results:
        if driver["@position"] == "1":
            number_of_laps = driver["Laps"]
    return number_of_laps


def laptimes_to_seconds(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["@time"] = (
        pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.minute * 60
        + pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.second
        + pd.to_datetime(dataframe["@time"], format="%M:%S.%f").dt.microsecond / 1000000
    )

    return dataframe
