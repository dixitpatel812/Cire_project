import mopy as mo
from pypsa import Network
import pandas as pd

heat_list = [['heat_boiler_oil', 'heat_boiler_gas'], ['heat_pump'], ["heat_storage"]]
hydrogen_list = [['steam_reforming'], ['electrolyser'], ['hydrogen_storage']]
electricity_list = [['solar', 'wind_offshore', 'wind_onshore', 'biomass', 'hydropower', 'lignite_coal', 'hard_coal', 'natural_gas'], ['heat_pump', 'electrolyser'], ['hydro_storage', 'battery_storage']]


def opt(net, opt_col_name):
    """
    :param net: network
    :param opt_col_name: name of the column
    :return: data frame
    """
    o = pd.DataFrame()
    o = mo.ver(o, net.generators.loc[:, "p_nom_opt"], net.links.loc[:, "p_nom_opt"], net.stores.loc[:, "e_nom_opt"])
    # o = o.loc[opt_file_list, :]
    o.columns = [str(opt_col_name) + "Mt"]
    return o


def energy(net, energy_list, ele=False):
    """
    :param net: network
    :param energy_list: nested list [[generators], [links], [stores]] of a specific energy bus
    :param ele: it provides additional constraint for electricity
    :return: energy data frame
    """
    e = pd.DataFrame(index=net.generators_t.p.index)
    # generator
    for i in energy_list[0]:
        if i in net.generators_t.p.columns:
            e = mo.hor(e, net.generators_t.p.loc[:, i])

    # link
    if ele:
        for i in energy_list[1]:
            if i in net.links_t.p0.columns:
                e = mo.hor(e, -net.links_t.p0.loc[:, i])
    else:
        for i in energy_list[1]:
            if i in net.links_t.p1.columns:
                e = mo.hor(e, abs(net.links_t.p1.loc[:, i]))

    # storage
    for i in energy_list[2]:
        if i in net.stores_t.p.columns:
            e = mo.hor(e, net.stores_t.p.loc[:, i])

    return e


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

    # creating data frames
    opt_file = pd.DataFrame()

    # input folder
    input_folder_path = mo.path.join(mo.input_path, data_folder_name)
    if not mo.path.isdir(input_folder_path):
        print("Error!!!! input_data_folder dose not exist")
        return

    #demand file
    demand_file_path = mo.path.join(input_folder_path, "loads-p_set.csv")
    demand_df = pd.read_csv(demand_file_path, index_col="name", parse_dates=True)

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

        # result folder
        result_folder_path = mo.path.join(output_folder_path, str(co2_limit))
        if not mo.path.isdir(result_folder_path):
            mo.mkdir(result_folder_path)

        # result files folder
        result_files_folder_path = mo.path.join(result_folder_path, "results")
        if not mo.path.isdir(result_files_folder_path):
            mo.mkdir(result_files_folder_path)

        # heat file
        heat = mo.hor(energy(network, heat_list), -demand_df.loc[:, "heat_demand"])
        heat.to_csv(mo.path.join(result_files_folder_path, "heat.csv"))

        # hydrogen file
        hydrogen = energy(network, hydrogen_list)
        hydrogen.to_csv(mo.path.join(result_files_folder_path, "hydrogen.csv"))

        # electricity file
        electricity = mo.hor(energy(network, electricity_list, ele=True), -demand_df.loc[:, "electricity_demand"])
        electricity.to_csv(mo.path.join(result_files_folder_path, "electricity.csv"))
        # opt file
        opt_file = mo.hor(opt_file, opt(network, co2_limit))

        # store output data?
        if output_data:
            network.export_to_csv_folder(result_folder_path)
        else:
            # if false then directly store the data that are important. (Ex: store, link and generators)
            pass

        # remove global constraint
        network.remove("GlobalConstraint", ["CO2_emission_limit"])

        # loop condition variable
        co2_limit = co2_limit - reduction
        # break

    # result files folder
    common_result_files_folder_path = mo.path.join(output_folder_path, "results")
    if not mo.path.isdir(common_result_files_folder_path):
        mo.mkdir(common_result_files_folder_path)

    # saving opt file
    opt_file.to_csv(mo.path.join(common_result_files_folder_path, "opt.csv"))


if __name__ == "__main__":
    # cire("old_t_0", start_limit=180, reduction=20, end_limit=80)
    # cire("old_t_0", start_limit=20, reduction=5, end_limit=0)
    cire("fi_0.0", start_limit=180, reduction=20, end_limit=80)
    cire("fi_0.0", start_limit=20, reduction=5, end_limit=0)

