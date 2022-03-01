import logging
from os import path, mkdir, listdir
from pandas import concat
import logging


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


def replace_with_space(text):
    text = text.replace("_", " ")
    return text

##############
# input_data_folder_name = "fi_4.0"
##############

input_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/"
output_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/"


def folder_exist_err(entire_path, folder_name, exist=True):
    if exist:
        if path.exists(path.join(entire_path, folder_name)):
            raise IOError('D8 : "%s" exist' % folder_name)
    else:
        if not path.exists(path.join(entire_path, folder_name)):
            raise IOError('D8 : "%s" does not exist' % folder_name)


# folder_exist_err(input_path, input_data_folder_name, exist=False)

# # make output folder
# # not needed here
# if not path.exists(path.join(output_path, input_data_folder_name)):
#     mkdir(path.join(output_path, input_data_folder_name))
#     logging.info(" D8 : creating output folder %s @ %s" % (input_data_folder_name, path.join(output_path, input_data_folder_name)))


# nested list with [[gen], [[out_link], [in_link]], [stores]]
# improvement :  think or implement how you can make these lists from input files
heat_list = [['heat_boiler_oil', 'heat_boiler_gas'], [["heat_charging"], ['heat_pump', "heat_discharging"]], ["heat_storage"]]
hydrogen_list = [['steam_reforming'], [['hydrogen_charging', "hydrogen_fuel_cell"], ['electrolyser', "hydrogen_discharging"]], ['hydrogen_storage']]
electricity_list = [['solar', 'wind_offshore', 'wind_onshore', 'biomass', 'hydropower', 'lignite_coal', 'hard_coal', 'natural_gas', "oil"], [['heat_pump', 'electrolyser', "battery_charging", "hydro_charging"], ["hydrogen_fuel_cell", "battery_discharging", "hydro_discharging"]], ['hydro_storage', 'battery_storage']]