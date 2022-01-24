from os import path, mkdir, listdir
import  pypsa
from pandas import concat


def hor(*x):
    """
    concat horizontally
    :param x: dataframe
    :return: dataframe
    """
    data = concat(x, axis=1)
    return data


def ver(*x):
    """
    concat vertically
    :param x: dataframe
    :return: dataframe
    """
    data = concat(x, axis=0)
    return data


input_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/"
output_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/"

input_data_folder_name = "fi_2.0.2"

# with fuel cell
heat_list = [['heat_boiler_oil', 'heat_boiler_gas'], [["heat_charging"], ['heat_pump', "heat_discharging"]], ["heat_storage"]]
hydrogen_list = [['steam_reforming'], [['hydrogen_charging', "hydrogen_fuel_cell"], ['electrolyser', "hydrogen_discharging"]], ['hydrogen_storage']]
electricity_list = [['solar', 'wind_offshore', 'wind_onshore', 'biomass', 'hydropower', 'lignite_coal', 'hard_coal', 'natural_gas', "oil"], [['heat_pump', 'electrolyser', "battery_charging", "hydro_charging"], ["hydrogen_fuel_cell", "battery_discharging", "hydro_discharging"]], ['hydro_storage', 'battery_storage']]

# without fuel cell
# heat_list = [['heat_boiler_oil', 'heat_boiler_gas'], [["heat_charging"], ['heat_pump', "heat_discharging"]], ["heat_storage"]]
# hydrogen_list = [['steam_reforming'], [['hydrogen_charging'], ['electrolyser', "hydrogen_discharging"]], ['hydrogen_storage']]
# electricity_list = [['solar', 'wind_offshore', 'wind_onshore', 'biomass', 'hydropower', 'lignite_coal', 'hard_coal', 'natural_gas'], [['heat_pump', 'electrolyser', "battery_charging", "hydro_charging"], ["battery_discharging", "hydro_discharging"]], ['hydro_storage', 'battery_storage']]