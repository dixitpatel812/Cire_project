import logging
import mopy as mo
from pypsa import Network
import pandas as pd

# output_folder_path = mo.path.join(mo.output_path, data_folder_name)
# common_folder = mo.path.join(mo.output_path, data_folder_name, "common")
# common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
# individual_folder = mo.path.join(mo.output_path, data_folder_name, "individual")
# pypsa_out_path = mo.path.join(mo.output_path, data_folder_name, "pypsa_out")

network_name = "moosces"


def opt(net, col_name):
    """
    :param net: network
    :param col_name: name of the column
    :return: data frame
    """
    o = pd.DataFrame()
    o = mo.ver(o, net.generators.loc[:, "p_nom_opt"], net.links.loc[:, "p_nom_opt"], net.stores.loc[:, "e_nom_opt"])
    # o.columns = [str(col_name) + "Mt"]
    o.columns = [str(col_name)]
    return o


def file(df, col_name, col_sum=True):
    """
    input files and give a changed dataframe with index and column
    :param df: dataframe
    :param col_name: str
    :param col_sum: allow to sum all the columns
    :return: dataframe
    """
    if col_sum:
        f = df.sum(axis=0)
    f = mo.hor(pd.DataFrame(), f)
    # f.columns = [str(col_name) + "Mt"]
    f.columns = [str(col_name)]
    return f


def costs(df, df_t, co2_limit, mc=False, st=False):
    """
    :param df: input dataframe
    :param df_t: output dataframe
    :param co2_limit: Co2 limit
    :param mc: marginal cost allowable
    :param st: storage allowable
    :return:
    """
    cost = pd.DataFrame(index=df.index)
    for j in df.index:
        if mc:
            marginal_cost = (df_t.loc[:, j] * df.loc[j, "marginal_cost"]).sum()
            cost.loc[j, co2_limit] = df.loc[j, "capital_cost"] * (
                    df.loc[j, "p_nom_opt"] - df.loc[j, "p_nom_min"]) + marginal_cost
        else:
            if st:
                cost.loc[j, co2_limit] = df.loc[j, "capital_cost"] * (
                        df.loc[j, "e_nom_opt"] - df.loc[j, "e_nom_min"])
            else:
                cost.loc[j, co2_limit] = df.loc[j, "capital_cost"] * (
                        df.loc[j, "p_nom_opt"] - df.loc[j, "p_nom_min"])
    return cost


def energy(net, energy_list):
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
    # link_p0
    for i in energy_list[1][0]:
        if i in net.links_t.p0.columns:
            e = mo.hor(e, -net.links_t.p0.loc[:, i])

    # link_p0
    for i in energy_list[1][1]:
        if i in net.links_t.p1.columns:
            e = mo.hor(e, -net.links_t.p1.loc[:, i])

    # storage
    for i in energy_list[2]:
        if i in net.stores_t.p.columns:
            e = mo.hor(e, abs(net.stores_t.p.loc[:, i]))
        if i in net.stores_t.e.columns:
            x = pd.DataFrame(index=e.index)
            x = mo.hor(x, net.stores_t.e.loc[:, i])
            x.columns = [i + "_energy"]
            e = mo.hor(e, x)
    return e

###########################


def my_network(input_folder_path):
    network = Network()
    network.import_from_csv_folder(input_folder_path)
    logging.info(" D8 : created %s network " % network_name)
    return network


def my_mkdir(folder, *folder_name, exist_err=False):
    # folder_path = str()
    for i in range(len(folder_name)):
        folder = mo.path.join(folder, folder_name[i])
        # folder_path = folder + folder_name[i]

    # if exist_err:
    #     mo.folder_exist_err(folder, folder_path, exist=True)
    if not mo.path.isdir(folder):
        mo.mkdir(folder)

    # folder_path = mo.path.join(folder, folder_path)

    return folder
###########################


def output(data_folder_name: object, start_limit: object = 180, reduction: object = 20, end_limit: object = 0,
           m_factor: object = 10e5,
           pypsa_output_data: object = True,
           ones: object = False, GC=True) -> object:
    """
    :param GC: global constraints available
    :param ones: run only one time
    :param data_folder_name: name of the folder where input files are stored
    :param start_limit: int value (in millions) of maximum allowable limit of total co2 emission in a time period. (Ex: in our case, total CO2 emission in a year 2030 (hourly resolved))
    :param reduction: Co2 emission reduction
    :param end_limit: stop limit of reduction
    :param m_factor: multiplication factor is 1000000
    :param pypsa_output_data: (bool) if true, gives output. otherwise, no output.
    :return: no return
    note: producing output of  both (start and end) limits
    """
    # input folder
    input_folder_path = mo.path.join(mo.input_path, data_folder_name)

    # # # folder creation / path creation
    # creating output folder
    output_folder_path = my_mkdir(mo.output_path, data_folder_name, exist_err=True)
    # output_folder_path = mo.path.join(mo.output_path, data_folder_name)
    # mo.folder_exist_err(mo.output_path, data_folder_name, exist=True)
    # logging.info(" D8 : creating %s folder in output_folder" % data_folder_name)
    # if not mo.path.isdir(output_folder_path):
    #     mo.mkdir(output_folder_path)

    # creating common folder
    common_folder = my_mkdir(mo.output_path, data_folder_name, "common")

    # common_folder = mo.path.join(mo.output_path, data_folder_name, "common")
    # if not mo.path.isdir(common_folder):
    #     mo.mkdir(common_folder)

    # common files folder
    common_files_folder = my_mkdir(mo.output_path, data_folder_name, "common", "files")
    # common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    # if not mo.path.isdir(common_files_folder):
    #     mo.mkdir(common_files_folder)

    # individual folder
    individual_folder = my_mkdir(mo.output_path, data_folder_name, "individual")
    # individual_folder = mo.path.join(mo.output_path, data_folder_name, "individual")
    # if not mo.path.isdir(individual_folder):
    #     mo.mkdir(individual_folder)

    # pypsa output folder
    pypsa_out_path = my_mkdir(mo.output_path, data_folder_name, "pypsa_out")
    # if pypsa_output_data:
    #     pypsa_out_path = mo.path.join(mo.output_path, data_folder_name, "pypsa_out")
    #     if not mo.path.isdir(pypsa_out_path):
    #         mo.mkdir(pypsa_out_path)

    # creating data frames
    cost = pd.DataFrame()
    opt_file = pd.DataFrame()
    electricity_total = pd.DataFrame()
    heat_total = pd.DataFrame()
    hydrogen_total = pd.DataFrame()

    # demand file
    demand_file_path = mo.path.join(input_folder_path, "loads-p_set.csv")
    demand_df = pd.read_csv(demand_file_path, index_col="name", parse_dates=True)

    # # # create PyPSA network
    network = Network()
    network.import_from_csv_folder(input_folder_path)
    logging.info(" D8 : created %s network " % network_name)

    co2_limit = start_limit

    while co2_limit >= end_limit:
        logging.info(f" D8 : simulation of {network_name} at {co2_limit}")

        # add global constraint
        if GC:
            network.add("GlobalConstraint", "CO2_emission_limit", type="primary_energy",
                        carrier_attribute="co2_emissions", constant=co2_limit * int(m_factor), sense="<=")

        network.lopf(network.snapshots, solver_name="gurobi_direct")

        # if not GC:
        #     co2_emission = 0
        #     n_re = {"Gas": ['natural_gas', 'steam_reforming', 'heat_boiler_gas'], "Oil": ['heat_boiler_oil', "oil"],
        #             "Lignite": ['lignite_coal'], "Hard_coal": ['hard_coal']}
        #
        #     for i in n_re.get("Gas"):
        #         if i in network.generators_t.p.columns:
        #             co2_emission = co2_emission + (network.generators_t.p.loc[:, i].sum() * network.carriers.loc[
        #                 "Gas", "co2_emissions"] / network.generators.loc[i, "efficiency"])
        #
        #     for i in n_re.get("Oil"):
        #         if i in network.generators_t.p.columns:
        #             co2_emission = co2_emission + (network.generators_t.p.loc[:, i].sum() * network.carriers.loc[
        #                 "Oil", "co2_emissions"] / network.generators.loc[i, "efficiency"])
        #
        #     for i in n_re.get("Lignite"):
        #         if i in network.generators_t.p.columns:
        #             co2_emission = co2_emission + (network.generators_t.p.loc[:, i].sum() * network.carriers.loc[
        #                 "Lignite", "co2_emissions"] / network.generators.loc[i, "efficiency"])
        #
        #     for i in n_re.get("Hard_coal"):
        #         if i in network.generators_t.p.columns:
        #             co2_emission = co2_emission + (network.generators_t.p.loc[:, i].sum() * network.carriers.loc[
        #                 "Hard_coal", "co2_emissions"] / network.generators.loc[i, "efficiency"])
        #
        #     return co2_emission

        # store output data?
        if pypsa_output_data:
            # pypsa result folder
            pypsa_co2limit_folder_path = mo.path.join(pypsa_out_path, str(co2_limit))
            mo.mkdir(pypsa_co2limit_folder_path)
            # store data
            network.export_to_csv_folder(pypsa_co2limit_folder_path)
        else:
            logging.warning(" D8 : not stored pypsa output")

        # d8 files folder ()
        d8_co2limit_folder_path = mo.path.join(individual_folder, str(co2_limit))
        if not mo.path.isdir(d8_co2limit_folder_path):
            mo.mkdir(d8_co2limit_folder_path)

        # heat file
        heat = mo.hor(energy(network, mo.heat_list), -demand_df.loc[:, "heat_demand"])
        heat.to_csv(mo.path.join(d8_co2limit_folder_path, "heat.csv"))

        heat_total = mo.hor(heat_total, file(heat, col_name=co2_limit, col_sum=True))

        # hydrogen file
        hydrogen = energy(network, mo.hydrogen_list)
        hydrogen["hydrogen_demand"] = -network.loads.loc["hydrogen_demand", "p_set"]
        hydrogen.to_csv(mo.path.join(d8_co2limit_folder_path, "hydrogen.csv"))

        hydrogen_total = mo.hor(hydrogen_total, file(hydrogen, col_name=co2_limit, col_sum=True))

        # electricity file
        electricity = mo.hor(energy(network, mo.electricity_list), -demand_df.loc[:, "electricity_demand"])
        electricity.to_csv(mo.path.join(d8_co2limit_folder_path, "electricity.csv"))

        electricity_total = mo.hor(electricity_total, file(electricity, col_name=co2_limit, col_sum=True))

        # opt file
        opt_file = mo.hor(opt_file, opt(network, co2_limit))

        # costs
        c = costs(network.generators, network.generators_t.p, str(co2_limit), mc=True)
        c = mo.ver(c, costs(network.links, network.links_t.p0, str(co2_limit), mc=False))
        c = mo.ver(c, costs(network.stores, network.stores_t.p, str(co2_limit), mc=False, st=True))
        cost = mo.hor(cost, c)

        # remove global constraint

        network.remove("GlobalConstraint", "CO2_emission_limit")

        # loop condition variable
        co2_limit = co2_limit - reduction
        if ones:
            break

    # saving opt file
    opt_file.to_csv(mo.path.join(common_files_folder, "opt.csv"))
    hydrogen_total.to_csv(mo.path.join(common_files_folder, "hydrogen_total.csv"))
    heat_total.to_csv(mo.path.join(common_files_folder, "heat_total.csv"))
    electricity_total.to_csv(mo.path.join(common_files_folder, "electricity_total.csv"))
    cost.to_csv(mo.path.join(common_files_folder, "cost.csv"))


if __name__ == "__main__":
    # folder_creation("test")
    output("fi_4.0", ones=False)
