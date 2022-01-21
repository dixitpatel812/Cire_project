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

input_data_folder_name = "fi_0.0"