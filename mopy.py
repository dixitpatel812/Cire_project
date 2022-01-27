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


##############
input_data_folder_name = "test"
##############

input_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/"
output_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/"

# check input folder (D8)
if not path.exists(path.join(input_path,input_data_folder_name)):
    raise IOError('D8 : "%s" does not exist' % input_data_folder_name)

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