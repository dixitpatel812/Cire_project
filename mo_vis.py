import mopy as mo


def vis(results_folder_path):
    output_folder_list = mo.listdir(mo.path.join(mo.output_path, mo.input_data_folder_name))


if __name__ == "__main__":
    result_data_folder_path = mo.path.join("/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/fi_0.0/", "result")
    vis(result_data_folder_path)
    pass