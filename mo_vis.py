import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt
import numpy as np

bar_colour = ["b", "g", "k", "m", "c", "r", "pink", "orange", "yellow"]


# heat
heat_in = ["heat_pump", "heat_boiler_oil", "heat_boiler_gas", "heat_discharging"]
heat_out = ["heat_demand", "heat_charging"]
heat_colour = ["b-", "g--", "k:", "m+", "c--", "r:"]

# hydrogen
# hydrogen_in = ["electrolyser", "steam_reforming", "hydrogen_discharging"]
# hydrogen_out = ["hydrogen_demand", "hydrogen_charging", "hydrogen_fuel_cell"]
hydrogen_in = ["electrolyser", "team_reforming", "hydrogen_dscharging"]
hydrogen_out = ["hydrogen_demand", "hyrogen_charging", "hydogen_fuel_cell"]
hydrogen_colour = ["b-", "g--", "k:", "m-", "c--", "r:"]

# electricity
electricity_in = ['biomass', 'hydropower', 'solar', 'wind_offshore', 'wind_onshore', 'lignite_coal', 'hard_coal', 'natural_gas', "oil", "battery_discharging", "hydro_discharging", "hydrogen_fuel_cell"]
electricity_out = ['heat_pump', 'electrolyser', "", "electricity_demand", "battery_charging", "hydro_charging"]
# electricity_colour = ["b-", "g--", "k:", "+m", "--c", ":r"]


def cum_sum_file(df, e_list):
    df_new = pd.DataFrame()

    for m in e_list:
        if m in df.columns:
            df_new = mo.hor(df_new, df.loc[:, m])

    df_new = df_new.cumsum(axis=1)
    return df_new


def file_hourly(in_folder_path, energy_file, e_list_in, e_list_out, out_file_name, out_folder_path, ele=False):
    c = 0
    df = pd.read_csv(mo.path.join(in_folder_path, energy_file), index_col="name", parse_dates=True)
    df_in = cum_sum_file(df, e_list_in)
    df_out = cum_sum_file(df, e_list_out)

    for i in df_in.columns:
        if ele:
            plt.plot(df_in.index, df_in.loc[:, i], label=i)
        else:
            plt.plot(df_in.index, df_in.loc[:, i], heat_colour[c], label=i)
            c = c+1
    for j in df_out.columns:
        if ele:
            plt.plot(df_out.index, df_out.loc[:, j], label=j)
        else:
            plt.plot(df_out.index, df_out.loc[:, j], heat_colour[c], label=j)
            c = c+1

    plt.title(out_file_name)
    plt.xlabel("time in hours")
    plt.ylabel("energy in MWh")
    plt.legend()
    plt.savefig(mo.path.join(out_folder_path, out_file_name + ".png"), dpi=600)
    plt.clf()
    # return


def cum_sum_file_total(df, e_list):
    df_new = pd.DataFrame(index=df.columns)

    for m in e_list:
        if m in df.index:
            df_new = mo.hor(df_new, df.loc[m, :])

    return df_new


def file_total(in_folder_path, energy_file_name, e_list_in, e_list_out, out_file_name, out_folder_path, ele=False):
    df = pd.read_csv(mo.path.join(in_folder_path, energy_file_name), index_col=0)

    df_in = cum_sum_file_total(df, e_list_in)
    df_out = cum_sum_file_total(df, e_list_out)

    X = np.arange(len(df_in.index))
    # lab = [df_in.columns[0]]
    plt.bar(X - 0.15, df_in.loc[:, df_in.columns[0]], width=.25)
    for i in range(1, len(df_in.columns)):
        plt.bar(X - 0.15, df_in.loc[:, df_in.columns[i]], width=.25, bottom=(df_in.loc[:, df_in.columns[:i]]).sum(axis=1))
        # lab.append(df_in.columns[i])

    X = np.arange(len(df_out.index))
    # lab = lab.append(df_out.columns[0])
    plt.bar(X + 0.15, abs(df_out.loc[:, df_out.columns[0]]), width=.25)
    for i in range(1, len(df_out.columns)):
        plt.bar(X + 0.15, abs(abs(df_out.loc[:, df_out.columns[i]])), width=.25, bottom=abs((df_out.loc[:, df_out.columns[:i]]).sum(axis=1)))
        # lab.append(df_out.columns[i])

    plt.title(out_file_name)
    plt.xlabel("CO2 limit in Mtons")
    plt.ylabel("annual energy in MWh")
    # plt.xticks(np.arange(len(df_in.index)+len(df_out.index)), np.arange(0, 180, 20))
    # plt.legend(lab)
    plt.savefig(mo.path.join(out_folder_path, out_file_name + ".png"), dpi=600)
    plt.clf()
    # return


def vis(data_folder_name, line=False, bar=False):
    if line:
        if mo.path.isdir(mo.path.join(mo.output_path, data_folder_name)):
            if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "electricity_bus")):
                mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "electricity_bus"))
            if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus")):
                mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus"))
            if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "heat_bus")):
                mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "heat_bus"))

            folder_list = mo.listdir(mo.path.join(mo.output_path, data_folder_name))
            folder_list.remove("results")
            for folder in folder_list:
                result_files_folder_path = mo.path.join(mo.path.join(mo.output_path, data_folder_name), folder, "results")
                # file_hourly(result_files_folder_path, "electricity.csv", electricity_in, electricity_out, folder + "_electricity_bus", mo.path.join(mo.output_path, data_folder_name, "results", "electricity_bus"), ele=True)
                # file_hourly(result_files_folder_path, "heat.csv", heat_in, heat_out, folder + "_heat_bus", mo.path.join(mo.output_path, data_folder_name, "results", "heat_bus"))
                file_hourly(result_files_folder_path, "hydrogen.csv", hydrogen_in, hydrogen_out, folder + "_hydrogen_bus", mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus"))
        else:
            print("Error!!! output folder path dose not exits")
            return
    if bar:
        common_result_files_folder_path = mo.path.join(mo.output_path, data_folder_name, "results")
        if not mo.path.isdir(common_result_files_folder_path):
            return
        file_total(common_result_files_folder_path, "heat_total.csv", heat_in, heat_out, "heat_total", common_result_files_folder_path)
        file_total(common_result_files_folder_path, "hydrogen_total.csv", hydrogen_in, hydrogen_out, "hydrogen_total", common_result_files_folder_path)
        file_total(common_result_files_folder_path, "electricity_total.csv", electricity_in, electricity_out, "electricity_total", common_result_files_folder_path)


if __name__ == "__main__":
    vis(mo.input_data_folder_name, line=True)
    # mo.input_data_folder_name