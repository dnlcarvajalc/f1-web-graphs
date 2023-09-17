import requests
import pandas as pd
import matplotlib.pyplot as plt
import xmltodict
import json

base_url = "https://ergast.com/api/f1/"

year_race = 2023
round_race = 1

def return_data_response(url:str):
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = xmltodict.parse(response.content)
        return data_dict
    else:
        print("Request failed with status code:", response.status_code)

def get_number_of_laps_done():
    endpoint = f'{year_race}/{round_race}/results'
    url = base_url + endpoint
    data_dict = return_data_response(url)

    driver_results = data_dict["MRData"]["RaceTable"]["Race"]["ResultsList"]["Result"]
    for driver in driver_results:
        if driver['@position'] == '1':
            number_of_laps = driver["Laps"]
    laps_dataframe = get_pandas_dataframe(number_of_laps)
    return laps_dataframe, number_of_laps

def get_pandas_dataframe(number_of_laps:int):
    all_laps_df = pd.DataFrame()
    for lap_number in range(1, int(number_of_laps) + 1):
        endpoint = f'{year_race}/{round_race}/laps/{lap_number}'
        url = base_url + endpoint
        data_dict = return_data_response(url)

        timing_data = data_dict["MRData"]["RaceTable"]["Race"]["LapsList"]["Lap"]["Timing"]
        one_lap_df = pd.DataFrame(timing_data)
        all_laps_df = pd.concat([all_laps_df, one_lap_df], axis=0)
   
    
    # Convert lap times to seconds for plotting
    all_laps_df['@time'] = pd.to_datetime(all_laps_df['@time'], format='%M:%S.%f').dt.minute * 60 + \
                           pd.to_datetime(all_laps_df['@time'], format='%M:%S.%f').dt.second + \
                           pd.to_datetime(all_laps_df['@time'], format='%M:%S.%f').dt.microsecond / 1000000
    
    return all_laps_df

def plot_single_driver(full_df, driver_name:str, color_plot:str, label_driver:str):
    driver_df_mask = full_df['@driverId'] == driver_name
    driver_df = pd.DataFrame()
    driver_df = full_df[driver_df_mask]
    plt.plot(driver_df['@lap'], driver_df['@time'], marker='.', linestyle='-', color=color_plot, label=label_driver)

if __name__ == "__main__":
    all_laps_df, number_of_laps = get_number_of_laps_done()
    # Plot lap times against laps
    plt.figure(figsize=(10, 6))
    plot_single_driver(all_laps_df, 'perez', 'b', 'Chequito BB')
    plot_single_driver(all_laps_df, 'max_verstappen', 'r', 'Srto Maximilian')
    plt.xlabel('Laps')
    plt.ylabel('Lap Time (seconds)')
    plt.title('Lap Times vs. Laps')
    plt.legend()
    plt.xticks(range(0, int(number_of_laps), 2))  # Display every 2nd label
    plt.grid(True)
    plt.show()