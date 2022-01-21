import pandas as pd
import mopy as mo


def vis(result_path):

    # output folder
    output_folder_path = mo.path.join(mo.output_path, mo.input_data_folder_name)
    if mo.path.isdir(output_folder_path):
        # list of folder inside the output folder
        output_folder_list = mo.listdir(output_folder_path)
        output_folder_list.remove("results")

        for co2_limit in output_folder_list:
            result_folder_path = mo.path.join(output_folder_path, co2_limit, "results")

    else:
        print("Error!!! output folder path dose not exits")
        return


if __name__ == "__main__":
    result_data_folder_path = mo.path.join(mo.output_path, mo.input_data_folder_name, "results")
    vis(result_data_folder_path)