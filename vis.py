import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt
import numpy as np
import logging


def cum_sum_file_total(df, e_list):
    df_new = pd.DataFrame(index=df.columns)

    for m in e_list:
        if m in df.index:
            df_new = mo.hor(df_new, df.loc[m, :])

    return df_new


def file_total(in_folder_path, energy_file_name, e_list_in, e_list_out, out_file_name, out_folder_path, ele=False):
    df = pd.read_csv(mo.path.join(in_folder_path, energy_file_name), index_col=0)

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
    plt.xlabel("CO2 limit in MTons")
    plt.ylabel("annual energy in MWh")
    plt.xticks(np.arange(len(df_in.index)), df_in.index, rotation="vertical")
    plt.legend(fontsize="xx-small")
    plt.savefig(mo.path.join(out_folder_path, out_file_name + ".png"), dpi=600)
    plt.clf()
    # return


# for stacked_energy_column_graph
colour_list = ["black", "gray", "darkgrey", "silver", "red", "green", "blue", "sienna", "orchid", "fuchsia", "salmon", "tomato", "peru", "khaki", "plum", "purple", "violet", "pink", "yellow"]

electricity_out = ['heat_pump', 'electrolyser', "", "electricity_demand"]
electricity_in = ['biomass', 'hydropower', 'solar', 'wind_offshore', 'wind_onshore', 'lignite_coal', 'hard_coal', 'natural_gas', "oil", "hydrogen_fuel_cell"]

hydrogen_in = ["electrolyser", "steam_reforming"]
hydrogen_out = ["hydrogen_demand", "hydrogen_fuel_cell"]

heat_in = ["heat_pump", "heat_boiler_oil", "heat_boiler_gas"]
heat_out = ["heat_demand"]


def stacked_energy_column_graph(data_folder_name):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    common_bar = mo.path.join(mo.output_path, data_folder_name, "common", "stacked_energy_column_graph")
    if not mo.path.isdir(common_files_folder):
        print("not found result folder")
        print("exit!!")
        return
    if not mo.path.isdir(common_bar):
        mo.mkdir(common_bar)
        print("creating common_bar folder")
    file_total(common_files_folder, "heat_total.csv", heat_in, heat_out, "heat_total",
               common_bar)
    print("created heat_total bar graph")
    file_total(common_files_folder, "hydrogen_total.csv", hydrogen_in, hydrogen_out, "hydrogen_total",
               common_bar)
    print("created hydrogen_total bar graph")
    file_total(common_files_folder, "electricity_total.csv", electricity_in, electricity_out,
               "electricity_total", common_bar)
    print("created electricity_total bar graph")


def vis_ind(data_frame, title, folder_path):
    for i in data_frame.index:
        plt.plot(data_frame.columns, data_frame.loc[i, :], label=i)
        plt.title(title + "  " + i)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("")
        plt.xticks(data_frame.columns, rotation="vertical")
        plt.subplots_adjust(bottom=.17)
        plt.savefig(mo.path.join(folder_path, title + "_" + i + ".png"))
        plt.clf()


comparison_list = ['solar', 'wind_offshore', 'wind_onshore', 'electrolyser', 'heat_pump', 'biomass', 'natural_gas']


def vis_comparison_ind(data_folder_name, c_list):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    common_folder = mo.path.join(mo.output_path, data_folder_name, "common")
    comparison_folder = mo.path.join(common_folder, "comparison")

    mo.folder_exist_err(common_folder, "comparison", exist=True)
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


def vis(data_folder_name, cost=False, curl=False, energy=False, opt=False):
    common_files_folder = mo.path.join(mo.output_path, data_folder_name, "common", "files")
    common_folder = mo.path.join(mo.output_path, data_folder_name, "common")

    if cost:
        cost = pd.read_csv(mo.path.join(common_files_folder, "cost.csv"), index_col=0)
        plt.plot(cost.columns, cost.sum(axis=0)/1e9)
        plt.xlabel("CO2 emission limit")
        plt.ylabel("Total cost in billion Euro")
        plt.xticks(rotation="vertical")
        plt.title("Cost of reducing CO2 emissions")
        mo.folder_exist_err(common_folder, 'cost.png', exist=True)
        plt.savefig(mo.path.join(common_folder, "cost.png"), dpi=600)
        plt.clf()

    if curl:
        curtail = pd.read_csv(mo.path.join(common_files_folder, "total_curtailments.csv"), index_col=0)
        plt.plot(curtail.columns, curtail.sum(axis=0) / 1e6)
        plt.xlabel("CO2 emission limit in MTons")
        plt.ylabel("Energy in GWh/year")
        plt.xticks(rotation="vertical")
        plt.title("Curtailed Electricity")
        mo.folder_exist_err(common_folder, 'curtailment.png', exist=True)
        plt.savefig(mo.path.join(common_folder, "curtailment.png"), dpi=600)
        plt.clf()

    if energy:
        electricity = pd.read_csv(mo.path.join(common_files_folder, "electricity_total.csv"), index_col=0)
        heat = pd.read_csv(mo.path.join(common_files_folder, "heat_total.csv"), index_col=0)
        hydrogen = pd.read_csv(mo.path.join(common_files_folder, "hydrogen_total.csv"), index_col=0)

        total_energy_folder_ind = mo.path.join(common_folder, "total_energy_ind")
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
        if not mo.path.isdir(mo.path.join(common_folder, "opt_ind")):
            mo.mkdir(mo.path.join(common_folder, "opt_ind"))
        vis_ind(opt_file, "opt", mo.path.join(common_folder, "opt_ind"))


if __name__ == "__main__":
    # stacked_energy_column_graph("fi_4.0")
    # vis("fi_4.0", curl=True, cost=True)
    vis_comparison_ind("fi_4.0", comparison_list)