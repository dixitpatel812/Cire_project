import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt
import numpy as np
import logging

colour_list = ["black", "gray", "darkgrey", "silver", "red", "green", "blue", "sienna", "orchid", "fuchsia", "salmon", "tomato", "peru", "khaki", "plum", "purple", "violet", "pink", "yellow"]

comparison_list = ["electrolyser", "solar", "biomass", "natural_gas", "lignite_coal", "hard_coal", 'hydropower']


def cum_sum_file_total(df, e_list):
    df_new = pd.DataFrame(index=df.columns)

    for m in e_list:
        if m in df.index:
            df_new = mo.hor(df_new, df.loc[m, :])

    return df_new


def vis_ind(data_frame, title, folder_path, ind=True):
    """
    :param data_frame: data frame with one row (axis=0) will be considered for plot at a time
    :param title: main title
    :param folder_path: out folder path
    :param ind: True (individual graph will be saved) , False (all in one graph will be saved)
    :return:
    """
    c = 3
    if ind:
        for i in data_frame.index:
            plt.plot(data_frame.columns, data_frame.loc[i, :], colour_list[c], label=i)
            plt.title(title + "  " + i)
            plt.xlabel("CO2_emission limit")
            plt.ylabel("")
            plt.xticks(data_frame.columns, rotation="vertical")
            plt.savefig(mo.path.join(folder_path, title + "_" + i + ".png"), dpi=400)
            plt.legend(fontsize="xx-small")
            plt.clf()
            c = c + 1
    if not ind:
        for i in data_frame.index:
            plt.plot(data_frame.columns, data_frame.loc[i, :], colour_list[c], label=i)
            c = c + 1
        plt.title(title)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("")
        plt.xticks(data_frame.columns, rotation="vertical")
        plt.legend(fontsize="xx-small")
        plt.savefig(mo.path.join(folder_path, title + ".png"), dpi=600)
        plt.clf()


def file_total(data_folder_name, csv_file_name, e_list_in, e_list_out, out_file_name, out_folder_path, ele=False):
    df = updated_energy(data_folder_name, csv_file_name, drooping=True, demand=False, loss=True)

    c = 0

    df_in = cum_sum_file_total(df, e_list_in)
    df_out = cum_sum_file_total(df, e_list_out)

    X = np.arange(len(df_in.index))
    # lab = [df_in.columns[0]]
    plt.bar(X - 0.15, df_in.loc[:, df_in.columns[0]], width=.25, label=df_in.columns[0])
    for i in range(1, len(df_in.columns)):
        c = c+1
        plt.bar(X - 0.15, df_in.loc[:, df_in.columns[i]], color=colour_list[c], width=.25, bottom=(df_in.loc[:, df_in.columns[:i]]).sum(axis=1), label=df_in.columns[i])
        # lab.append(df_in.columns[i])

    X = np.arange(len(df_out.index))
    # lab = lab.append(df_out.columns[0])
    c = c+1
    plt.bar(X + 0.15, abs(df_out.loc[:, df_out.columns[0]]), width=.25, label=df_out.columns[0])
    for i in range(1, len(df_out.columns)):
        c = c+1
        plt.bar(X + 0.15, abs(abs(df_out.loc[:, df_out.columns[i]])), width=.25, bottom=abs((df_out.loc[:, df_out.columns[:i]]).sum(axis=1)), label=df_out.columns[i])
        # lab.append(df_out.columns[i])

    plt.title(out_file_name)
    plt.xlabel("CO2 limit (MTons)")
    plt.ylabel("Energy (MWh)")
    plt.xticks(np.arange(len(df_in.index)), df_in.index, rotation="vertical")
    plt.legend(fontsize="xx-small")
    plt.savefig(mo.path.join(out_folder_path, out_file_name + ".png"), dpi=600)
    plt.clf()
    # return


# for stacked_total_energy_column_graph

electricity_in = ['biomass', 'hydropower', 'solar', 'wind_offshore', 'wind_onshore', 'lignite_coal', 'hard_coal', 'natural_gas', "oil", "hydrogen_fuel_cell"]
electricity_out = ['heat_pump', 'electrolyser', "electricity_demand", "losses"]

hydrogen_in = ["electrolyser", "steam_reforming"]
hydrogen_out = ["hydrogen_demand", "losses", "hydrogen_fuel_cell"]

heat_in = ["heat_pump", "heat_boiler_oil", "heat_boiler_gas"]
heat_out = ["heat_demand", "losses"]


def stacked_total_energy_column_graph(data_folder_name):
    vis_folder = mo.path.join(mo.output_path, data_folder_name, "vis", "stacked_total_energy_column_graph")
    mo.folder_exist_err(mo.path.join(mo.output_path, data_folder_name, "vis"), "stacked_total_energy_column_graph", exist=True)
    if not mo.path.isdir(vis_folder):
        mo.mkdir(vis_folder)
    file_total(data_folder_name, "heat_total.csv", heat_in, heat_out, "heat_total", vis_folder)
    print("created heat_total bar graph")
    file_total(data_folder_name, "hydrogen_total.csv", hydrogen_in, hydrogen_out, "hydrogen_total", vis_folder)
    print("created hydrogen_total bar graph")
    file_total(data_folder_name, "electricity_total.csv", electricity_in, electricity_out, "electricity_total", vis_folder)
    print("created electricity_total bar graph")


def updated_energy(data_folder_name, csv_file_name, drooping=False, loss=False, demand=False):
    """
    :param demand: allow remove demand
    :param loss: allow loss [charging + discharging]
    :param drooping: allow removing [charging and discharging]
    :param data_folder_name: input folder name
    :param csv_file_name: fine name of the total energy file
    :return: dataframe  with removed store
    """

    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    energy = pd.read_csv(mo.path.join(common_files_folder, csv_file_name), index_col=0)

    cd = pd.DataFrame(index=energy.columns)
    # remove charging, discharging and store
    for i in energy.index:
        if "storage" in i:
            energy = energy.drop(i, axis=0)
        if drooping:
            if demand:
                if "demand" in i:
                    energy = energy.drop([i], axis=0)
            if "discharging" in i:
                cd = mo.hor(cd, energy.loc[i, :])
                energy = energy.drop(i, axis=0)
            elif "charging" in i:
                cd = mo.hor(cd, energy.loc[i, :])
                energy = energy.drop(i, axis=0)
    if loss:
        loss_s = cd.sum(axis=1)
        loss_s.name = "losses"
        energy = mo.hor(energy.T, loss_s)
        energy = energy.T
    return energy


def energy_line_graph(data_folder_name, csv_file_name):
    vis_folder = mo.path.join(mo.output_path, data_folder_name, "vis")
    line_graph_folder = mo.path.join(vis_folder, "total_energy_line_graph")
    # mo.folder_exist_err(vis_folder, "total_energy_line_graph")
    if not mo.path.exists(line_graph_folder):
        mo.mkdir(line_graph_folder)
    energy = updated_energy(data_folder_name, csv_file_name, drooping=True, demand=False, loss=True)
    vis_ind(energy, csv_file_name[:-4], line_graph_folder, ind=False)


def vis_comparison_ind(data_folder_name, c_list):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    vis_folder = mo.path.join(mo.output_path, data_folder_name, "vis")
    comparison_folder = mo.path.join(vis_folder, "comparison")

    mo.folder_exist_err(vis_folder, "comparison", exist=True)
    mo.mkdir(mo.path.join(comparison_folder))

    electricity = pd.read_csv(mo.path.join(common_files_folder, "electricity_total.csv"), index_col=0)
    # heat = pd.read_csv(mo.path.join(common_files_folder, "heat_total.csv"), index_col=0)
    # hydrogen = pd.read_csv(mo.path.join(common_files_folder, "hydrogen_total.csv"), index_col=0)

    opt_file = pd.read_csv(mo.path.join(common_files_folder, "opt.csv"), index_col=0)

    for i in c_list:
        df = pd.DataFrame(index=electricity.columns)
        df = mo.hor(df, abs(electricity.loc[i, :]), opt_file.loc[i, :])
        df.columns = ["total_energy_"+i, "opt_"+i]
        df = df.T
        mo.folder_exist_err(comparison_folder, i, exist=True)
        i_th_folder = mo.path.join(comparison_folder, i)
        mo.mkdir(i_th_folder)
        vis_ind(df, "", i_th_folder)


electricity_opt = ['biomass', 'hydropower',  'wind_offshore', '', 'lignite_coal', 'hard_coal', 'natural_gas', "oil", 'electrolyser']
electricity_opt_other = ['solar', "wind_onshore", "heat_pump" ]
hydrogen_opt = ["electrolyser", "steam_reforming"]
heat_opt = ["heat_pump", "heat_boiler_oil", "heat_boiler_gas"]
storage_opt = ["hydrogen_storage", "heat_storage", "battery_storage", "hydro_storage" ]


def opt_line_graph(data_folder_name, opt_list, title):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    opt_line_graph_folder = mo.path.join(mo.output_path, data_folder_name, "vis", "opt_line_graph")
    if not mo.path.exists(opt_line_graph_folder):
        mo.mkdir(opt_line_graph_folder)
    opt_file = pd.read_csv(mo.path.join(common_files_folder, "opt.csv"), index_col=0)
    c = 3
    for m in opt_list:
        if m in opt_file.index:
            plt.plot(opt_file.columns, opt_file.loc[m, :], colour_list[c], label=m)
            c = c + 1
    plt.title(title)
    plt.xlabel("CO2_emission limit")
    plt.ylabel("Installed capacity (MW)")
    plt.xticks(opt_file.columns, rotation="vertical")
    plt.legend(fontsize="xx-small")
    plt.savefig(mo.path.join(opt_line_graph_folder, title + ".png"), dpi=400)
    plt.clf()


def vis(data_folder_name, cost=False, curl=False, energy=False, opt=False, stacked_energy_column_graph=False, opt_lines=False, energy_lines=False):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    vis_folder = mo.path.join(mo.output_path, data_folder_name, "vis")
    if not mo.path.exists(vis_folder):
        mo.mkdir(vis_folder)

    if cost:
        cost = pd.read_csv(mo.path.join(common_files_folder, "cost.csv"), index_col=0)
        plt.plot(cost.columns, cost.sum(axis=0)/1e9)
        plt.xlabel("CO2 emission limit (MTon)")
        plt.ylabel("Total cost (Billion)")
        plt.xticks(rotation="vertical")
        plt.title("Cost of reducing CO2 emissions")
        mo.folder_exist_err(vis_folder, 'cost.png', exist=True)
        plt.savefig(mo.path.join(vis_folder, "cost.png"), dpi=600)
        plt.clf()

    if curl:
        curtail = pd.read_csv(mo.path.join(common_files_folder, "total_curtailments.csv"), index_col=0)
        plt.plot(curtail.columns, curtail.sum(axis=0) / 1e6)
        plt.xlabel("CO2 emission limit (MTon)")
        plt.ylabel("Energy (TWh/year)")
        plt.xticks(rotation="vertical")
        plt.title("Curtailed Electricity")
        mo.folder_exist_err(vis_folder, 'curtailment.png', exist=True)
        plt.savefig(mo.path.join(vis_folder, "curtailment.png"), dpi=600)
        plt.clf()

    if energy:
        electricity = pd.read_csv(mo.path.join(common_files_folder, "electricity_total.csv"), index_col=0)
        heat = pd.read_csv(mo.path.join(common_files_folder, "heat_total.csv"), index_col=0)
        hydrogen = pd.read_csv(mo.path.join(common_files_folder, "hydrogen_total.csv"), index_col=0)

        total_energy_folder_ind = mo.path.join(vis_folder, "total_energy_ind")
        if not mo.path.isdir(total_energy_folder_ind):
            mo.mkdir(total_energy_folder_ind)

        if not mo.path.isdir(mo.path.join(total_energy_folder_ind, "electricity_total_ind")):
            mo.mkdir(mo.path.join(total_energy_folder_ind, "electricity_total_ind"))
        vis_ind(abs(electricity), "electricity_total", mo.path.join(total_energy_folder_ind, "electricity_total_ind"))

        if not mo.path.isdir(mo.path.join(total_energy_folder_ind, "hydrogen_total_ind")):
            mo.mkdir(mo.path.join(total_energy_folder_ind, "hydrogen_total_ind"))
        vis_ind(abs(hydrogen), "hydrogen_total", mo.path.join(total_energy_folder_ind, "hydrogen_total_ind"))

        if not mo.path.isdir(mo.path.join(total_energy_folder_ind, "heat_total_ind")):
            mo.mkdir(mo.path.join(total_energy_folder_ind, "heat_total_ind"))
        vis_ind(abs(heat), "heat_total", mo.path.join(total_energy_folder_ind, "heat_total_ind"))

    if opt:
        opt_file = pd.read_csv(mo.path.join(common_files_folder, "opt.csv"), index_col=0)
        if not mo.path.isdir(mo.path.join(vis_folder, "opt_ind")):
            mo.mkdir(mo.path.join(vis_folder, "opt_ind"))
        vis_ind(opt_file, "opt", mo.path.join(vis_folder, "opt_ind"))

    if stacked_energy_column_graph:
        stacked_total_energy_column_graph(data_folder_name)

    if opt_lines:
        opt_line_graph(data_folder_name, heat_opt, "Heat")
        opt_line_graph(data_folder_name, hydrogen_opt, "Hydrogen")
        opt_line_graph(data_folder_name, electricity_opt, "Electricity")
        opt_line_graph(data_folder_name, electricity_opt_other, "Electricity_other")
        opt_line_graph(data_folder_name, storage_opt, "Storage")

    if energy_lines:
        energy_line_graph(data_folder_name, "electricity_total.csv")
        energy_line_graph(data_folder_name, "heat_total.csv")
        energy_line_graph(data_folder_name, "hydrogen_total.csv")


# not important anymore
def curtailment_bar_graph(data_folder_name):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    common_folder = mo.path.join(mo.output_path, data_folder_name, "common")

    curtail = pd.read_csv(mo.path.join(common_files_folder, "total_curtailments.csv"), index_col=0)/1e6

    x = np.arange(len(curtail.columns))

    c = 5
    plt.bar(x - 0.22, curtail.loc["solar", :], color=colour_list[c], width=.20, label="solar")

    c = c+1
    plt.bar(x, curtail.loc["wind_offshore", :], color=colour_list[c], width=.20, label="wind_offshore")

    c = c+1
    plt.bar(x + 0.22, curtail.loc["wind_onshore", :], color=colour_list[c], width=.20, label="wind_onshore")

    plt.title("curtailed energy")
    plt.xlabel("CO2 emission in MTons")
    plt.ylabel("Energy in TWh")
    plt.xticks(np.arange(len(curtail.columns)), curtail.columns, rotation="vertical")
    plt.legend(fontsize="x-small")
    # plt.show()
    plt.savefig(mo.path.join(common_folder, "curtailment_bar" + ".png"), dpi=600)
    plt.clf()


def cycle_bar_graph(data_folder_name):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    vis_folder = mo.path.join(mo.output_path, data_folder_name, "vis")

    cy = pd.read_csv(mo.path.join(common_files_folder, "storage_cycles.csv"), index_col=0)

    x = np.arange(len(cy.columns))

    c = 5
    plt.bar(x - 0.24, cy.loc["hydro_storage", :], color=colour_list[c], width=.12, label="hydro_storage")

    c = c+1
    plt.bar(x - .08, cy.loc["battery_storage", :], color=colour_list[c], width=.12, label="battery_storage")

    c = c + 1
    plt.bar(x + .08, cy.loc["heat_storage", :], color=colour_list[c], width=.12, label="heat_storage")

    c = c+1
    plt.bar(x + 0.24, cy.loc["hydrogen_storage", :], color=colour_list[c], width=.12, label="hydrogen_storage")

    plt.title("storage cycles")
    plt.xlabel("CO2 emission in MTons")
    plt.ylabel("number of cycles in a year")
    plt.xticks(np.arange(len(cy.columns)), cy.columns, rotation="vertical")
    plt.legend(fontsize="x-small")
    # plt.show()
    plt.savefig(mo.path.join(vis_folder, "cycle_bar" + ".png"), dpi=600)
    plt.clf()

    vis_ind(cy, "Storage_Cycles", vis_folder, ind=False)



if __name__ == "__main__":
    # stacked_total_energy_column_graph("fi_4.0.1")
    # vis("fi_4.0", curl=True, cost=True)
    # vis("fi_4.0", opt_lines=True)
    # opt_line_graph("fi_4.0", heat_opt, "Heat")
    # opt_line_graph("fi_4.0", hydrogen_opt, "Hydrogen")
    # opt_line_graph("fi_4.0", electricity_opt, "Electricity")
    # opt_line_graph("fi_4.0", electricity_opt_other, "Electricity_other")
    # opt_line_graph("fi_4.0", storage_opt, "Storage")
    # vis_comparison_ind("fi_4.0.1", comparison_list)


    # curtailment_bar_graph("fi_4.0.1")
    pass