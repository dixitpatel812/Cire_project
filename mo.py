import mopy as mo
from pypsa import Network
import pandas as pd


def opt(net, col_name):
    """
    :param net: network
    :param col_name: name of the column
    :return: data frame
    """
    o = pd.DataFrame()
    o = mo.ver(o, net.generators.loc[:, "p_nom_opt"], net.links.loc[:, "p_nom_opt"], net.stores.loc[:, "e_nom_opt"])
    o.columns = [str(col_name) + "Mt"]
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
    f.columns = [str(col_name) + "Mt"]
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
            e = mo.hor(e, net.stores_t.p.loc[:, i])
        if i in net.stores_t.e.columns:
            x = pd.DataFrame(index=e.index)
            x = mo.hor(x, net.stores_t.e.loc[:, i])
            x.columns = [i + "_energy"]
            e = mo.hor(e, x)
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
    cost = pd.DataFrame()
    opt_file = pd.DataFrame()
    electricity_total = pd.DataFrame()
    heat_total = pd.DataFrame()
    hydrogen_total = pd.DataFrame()

    # input folder
    input_folder_path = mo.path.join(mo.input_path, data_folder_name)
    if not mo.path.isdir(input_folder_path):
        print("Error!!!! input_data_folder dose not exist")
        return

    # demand file
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
        heat = mo.hor(energy(network, mo.heat_list), -demand_df.loc[:, "heat_demand"])
        heat_total = mo.hor(heat_total, file(heat, col_name=co2_limit, col_sum=True))
        heat.to_csv(mo.path.join(result_files_folder_path, "heat.csv"))

        # hydrogen file
        hydrogen = energy(network, mo.hydrogen_list)
        hydrogen["hydrogen_demand"] = -network.loads.loc["hydrogen_demand", "p_set"]
        hydrogen_total = mo.hor(hydrogen_total, file(hydrogen, col_name=co2_limit, col_sum=True))
        hydrogen.to_csv(mo.path.join(result_files_folder_path, "hydrogen.csv"))

        # electricity file
        electricity = mo.hor(energy(network, mo.electricity_list), -demand_df.loc[:, "electricity_demand"])
        electricity_total = mo.hor(electricity_total, file(electricity, col_name=co2_limit, col_sum=True))
        electricity.to_csv(mo.path.join(result_files_folder_path, "electricity.csv"))


        # opt file
        opt_file = mo.hor(opt_file, opt(network, co2_limit))

        # store output data?
        if output_data:
            network.export_to_csv_folder(result_folder_path)
        else:
            # if false then directly store the data that are important. (Ex: store, link and generators)
            pass

        # costs
        c = costs(network.generators, network.generators_t.p, str(co2_limit), mc=True)
        c = mo.ver(c, costs(network.links, network.links_t.p0, str(co2_limit), mc=False))
        c = mo.ver(c, costs(network.stores, network.stores_t.p, str(co2_limit), mc=False, st=True))
        cost = mo.hor(cost, c)

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
    hydrogen_total.to_csv(mo.path.join(common_result_files_folder_path, "hydrogen_total.csv"))
    heat_total.to_csv(mo.path.join(common_result_files_folder_path, "heat_total.csv"))
    electricity_total.to_csv(mo.path.join(common_result_files_folder_path, "electricity_total.csv"))
    cost.to_csv(mo.path.join(common_result_files_folder_path, "cost.csv"))


if __name__ == "__main__":
    cire(mo.input_data_folder_name, reduction=5)