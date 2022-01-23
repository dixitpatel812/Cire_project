import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt

# heat
heat_in = ["heat_pump", "heat_boiler_oil", "heat_boiler_gas", "heat_discharging"]
heat_out = ["heat_demand", "heat_charging"]
heat_colour = ["b-", "g--", "k:", "m+", "c--", "r:"]

# hydrogen
# hydrogen_in = ["electrolyser", "steam_reforming", "hydrogen_discharging"]
# hydrogen_out = ["hydrogen_demand", "hydrogen_charging", "hydrogen_fuel_cell"]

hydrogen_in = ["electrolyser", "steam_reforming", "hydrogen_dischargin"]
hydrogen_out = ["hydrogen_deand", "hydrogen_chargin", "hydrogen_fuel_cell"]

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


def file_hourly(in_folder_path, energy_file, e_list_in, e_list_out, out_file_name, out_folder_path):
    c = 0
    df = pd.read_csv(mo.path.join(in_folder_path, energy_file), index_col="name", parse_dates=True)
    df_in = cum_sum_file(df, e_list_in)
    df_out = cum_sum_file(df, e_list_out)

    for i in df_in.columns:
        plt.plot(df.index, df.loc[:, i], heat_colour[c], label=i)
        c = c+1
    for j in df_out.columns:
        plt.plot(df.index, df.loc[:, j], heat_colour[c], label=j)
        c = c+1

    plt.title(out_file_name)
    plt.xlabel("time in hours")
    plt.ylabel("energy in MWh")
    plt.legend()
    plt.savefig(mo.path.join(out_folder_path, out_file_name + ".png"), dpi=600)
    plt.clf()
    # return


def vis(data_folder_name):
    if mo.path.isdir(mo.path.join(mo.output_path, data_folder_name)):
        if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "electricity_bus")):
            mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "electricity_bus"))
        if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus")):
            mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus"))
        if not mo.path.isdir(mo.path.join(mo.output_path, data_folder_name, "results", "heat_bus")):
            mo.mkdir(mo.path.join(mo.output_path, data_folder_name, "results", "heat_bus"))

        folder_list = mo.listdir(mo.path.join(mo.output_path, data_folder_name))
        folder_list.remove("results")
        print(folder_list)
        for folder in folder_list:
            result_files_folder_path = mo.path.join(mo.path.join(mo.output_path, data_folder_name), folder, "results")

            # file_hourly(result_files_folder_path, "electricity.csv", electricity_in, electricity_out, "electricity_bus")
            # file_hourly(result_files_folder_path, "heat.csv", heat_in, heat_out, "heat_bus")
            file_hourly(result_files_folder_path, "hydrogen.csv", hydrogen_in, hydrogen_out, folder + "_hydrogen_bus", mo.path.join(mo.output_path, data_folder_name, "results", "hydrogen_bus"))
    else:
        print("Error!!! output folder path dose not exits")
        return


if __name__ == "__main__":
    common_result_files_folder_path = mo.path.join(mo.output_path, mo.input_data_folder_name, "results")
    vis(mo.input_data_folder_name)