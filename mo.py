import mopy as mo
from pypsa import Network


def cire(data_folder_name, co2_limit):
    """
    :param data_folder_name: name of the folder where input files are stored
    :param co2_limit: int value (in millions) of maximum allowable limit of total co2 emission in a time period. (Ex: in our case, total CO2 emission in a year 2030 (hourly resolved))
    :return:
    """

    co2_limit = co2_limit * 10e6

    # input folder
    input_folder_path = mo.path.join(mo.input_path, data_folder_name)
    if not mo.path.isdir(input_folder_path):
        print("Error???? input_data_folder dose not exist")
        return

    # output folder
    output_folder_path = mo.path.join(mo.output_path, data_folder_name)
    if not mo.path.isdir(output_folder_path):
        mo.mkdir(output_folder_path)

    # result folder
    result_folder_path = mo.path.join(output_folder_path, str(co2_limit))
    if not mo.path.isdir(result_folder_path):
        mo.mkdir(result_folder_path)
    # create PyPSA network
    network = Network()
    network.import_from_csv_folder(input_folder_path)

    while co2_limit >= 0:
        # add global constraint
        network.add("GlobalConstraint", "CO2_emission_limit", type="primary_energy", carrier_attribute="co2_emissions", constant=co2_limit, sense="<=")
        network.lopf(network.snapshots, solver_name="gurobi_direct")
        network.export_to_csv_folder(result_folder_path)
        network.remove("GlobalConstraint", ["CO2_emission_limit"])
        break


if __name__ == "__main__":
    cire("old_0.1.0", 18)
