import mopy as mo
from pypsa import Network


def cire(data_folder_name, start_limit=180, reduction=20, end_limit=0, m_factor=10e5, output_data=True):
    """
    :param data_folder_name: name of the folder where input files are stored
    :param start_limit: int value (in millions) of maximum allowable limit of total co2 emission in a time period. (Ex: in our case, total CO2 emission in a year 2030 (hourly resolved))
    :param reduction: Co2 emission reduction
    :param end_limit: stop limit of reduction
    :param m_factor: multiplication factor is 1000000
    :param output_data: (bool) if true, gives output. otherwise, no output.
    :return: no return
    note: producing output of  both (start and end) limits
    """
    # start_limit as co2 limit at a point
    co2_limit = start_limit

    # input folder
    input_folder_path = mo.path.join(mo.input_path, data_folder_name)
    if not mo.path.isdir(input_folder_path):
        print("Error!!!! input_data_folder dose not exist")
        return

    # output folder
    output_folder_path = mo.path.join(mo.output_path, data_folder_name)
    if not mo.path.isdir(output_folder_path):
        mo.mkdir(output_folder_path)

    # create PyPSA network
    network = Network()
    network.import_from_csv_folder(input_folder_path)

    while co2_limit >= end_limit:

        # add global constraint
        network.add("GlobalConstraint", "CO2_emission_limit", type="primary_energy", carrier_attribute="co2_emissions",
                    constant=co2_limit * int(m_factor), sense="<=")
        network.lopf(network.snapshots, solver_name="gurobi_direct")

        # store output data?
        if output_data:
            # result folder
            result_folder_path = mo.path.join(output_folder_path, str(co2_limit))
            if not mo.path.isdir(result_folder_path):
                mo.mkdir(result_folder_path)

            network.export_to_csv_folder(result_folder_path)
        else:
            # if false then directly store the data that are important. (Ex: store, link and generators)
            pass

        # remove global constraint
        network.remove("GlobalConstraint", ["CO2_emission_limit"])

        # loop condition variable
        co2_limit = co2_limit - reduction


if __name__ == "__main__":
    # cire("old_t_0", start_limit=180, reduction=20, end_limit=80)
    # cire("old_t_0", start_limit=60, reduction=5, end_limit=0)
