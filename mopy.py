import pandas as pd
from os import path
import matplotlib.pyplot as plt


def hor(*x):
    data = pd.concat(x, axis=1)
    return data


def ver(*x):
    data = pd.concat(x, axis=0)
    return data


def vis_all(data_frame, title, folder_path):
    for i in data_frame.index:
        plt.plot(data_frame.columns, data_frame.loc[i, :], label=i)
    plt.xticks(data_frame.columns, rotation="vertical")
    plt.title(title)
    plt.xlabel("CO2_emission limit")
    plt.ylabel("MWh")
    plt.legend()
    plt.subplots_adjust(bottom=.17)
    plt.savefig(path.join(folder_path, title + ".png"))
    plt.clf()


def vis_ind(data_frame, title, folder_path):
    for i in data_frame.index:
        plt.plot(data_frame.columns, data_frame.loc[i, :], label=i)
        plt.title(i)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("MWh")
        plt.xticks(data_frame.columns, rotation="vertical")
        plt.subplots_adjust(bottom=.17)
        plt.savefig(path.join(folder_path, title + "_" + i + ".png"))
        plt.clf()


#
# def gen_data(*x):
#     y = {"p_nom": x[0], "marginal_cost":x[1], "efficiency":x[2], "capital_cost":x[3], "p_nom_max":x[4], "p_nom_min":x[5], "p_max_pu":x[6]}
#     return y
#
# def sto_data(*z):
#     y = {"e_nom":z[0], "marginal_cost":z[1], "standing_loss":z[2], "capital_cost":z[3], "e_nom_max":z[4], "efficiency":z[5]}
#     return y
#
# def link_data(*a):
#     y = {"p_nom": a[0], "marginal_cost":a[1], "efficiency":a[2], "capital_cost":a[3], "p_nom_max":a[4]}
#     return y
#
# def tech(folder_path, file_name, tech):
#
#
#
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     if tech in data_file.columns:
#         data = data_file[tech]
#         data = data.sum(axis=0)
#     else:
#         data = 0
#     return data
#
# def read_file(folder_path, file_name, col="time", p=True):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col=col, parse_dates=p)
#     return data_file
#
# def mtech(folder_path, file_name, tech):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     x = {}
#     for t in tech:
#         if t in data_file.columns:
#             data = data_file[t]
#             data = data.sum(axis=0)
#             x[t] = round(abs(data),3)
#         else:
#             x[t] = 0
#     return x
#
# def link_mtech(folder_path, file_name, tech, string):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     x = {}
#     for t in tech:
#         if t in data_file.columns:
#             data = data_file[t]
#             data = data.sum(axis=0)
#             x[t+"_"+string] = round(abs(data),3)
#         else:
#             x[t+"_"+string] = 0
#     return x
#
# def link_tech(folder_path, file_name, tech, string):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     x = {}
#     if tech in data_file.columns:
#         data = data_file[tech]
#         data = data.sum(axis=0)
#         x[tech+"_"+string] = round(abs(data),3)
#     else:
#         x[tech+"_"+string] = 0
#     return x
#
# def tech_store(folder_path, file_name, tech):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     if tech in data_file.columns:
#         data = data_file[tech]
#         data = pd.concat([data[data<0], data[data>=0]], axis=1)
#         data.columns = ["c", "d"]
#         data_c = round(abs(data.c.sum(axis=0)),3)
#         data_d = round(abs(data.d.sum(axis=0)),3)
#     else:
#         data_c = 0
#         data_d = 0
#     return data_c, data_d
#
# def mtech_store(folder_path, file_name, tech):
#     data_file = pd.read_csv(os.path.join(folder_path, file_name), index_col="time", parse_dates=True)
#     x = {}
#     for t in tech:
#         if t in data_file.columns:
#             data = data_file[t]
#             data = pd.concat([data[data<0], data[data>=0]], axis=1)
#             data.columns = [t + "_charging", t + "_discharging"]
#             x[t + "_charging"] = round(abs(data[t + "_charging"].sum(axis=0)),3)
#             x[t + "_discharging"] = round(abs(data[t + "_discharging"].sum(axis=0)),3)
#         else:
#             x[t + "_charging"] = 0
#             x[t + "_discharging"] = 0
#     return x


def time_division(data_frame, hours, avg=False):
    """derive specific data (i.e. daily and weekly) data from hourly data"""
    rand = []
    division = pd.DataFrame()
    for n in range(len(data_frame.columns)):
        rand.append(list())
    for m in range(len(rand)):
        for i in range(0, 8760, hours):
            if avg:
                rand[m].append(data_frame.iloc[i:i + hours, m].sum() / hours)
            else:
                rand[m].append(data_frame.iloc[i:i + hours, m].sum())
        division[data_frame.columns[m]] = rand[m]
    division.index.name = "time"
    if len(division.index) > (8760 // hours):
        division = division.drop(division.index[-1], axis=0)
    return division


def plot_con(ti, x_lab, y_lab, folder_path):
    plt.title(ti)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.legend()
    plt.savefig(path.join(folder_path, ti + ".png"), dpi=600)
    plt.clf()


def graph(output_folder_name):
    output_folder = path.join("/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/", output_folder_name)
    list_dir = os.listdir(output_folder)
    folders = list()

    for i in range(len(list_dir)):
        if list_dir[i].isdigit():
            folders.append(list_dir[i])

    for folder_name in folders:
        folder_path = path.join(output_folder, folder_name)
        gen_p = pd.read_csv(path.join(folder_path, "generators-p.csv"), index_col="name", parse_dates=True)
        link_p_out = pd.read_csv(path.join(folder_path, "links-p1.csv"), index_col="name", parse_dates=True)
        link_p_in = pd.read_csv(path.join(folder_path, "links-p0.csv"), index_col="name", parse_dates=True)
        store_e = pd.read_csv(path.join(folder_path, "stores-e.csv"), index_col="name", parse_dates=True)
        store_p = pd.read_csv(path.join(folder_path, "stores-p.csv"), index_col="name", parse_dates=True)

        heat = pd.DataFrame(index=demand_df.index)
        if "heat_boiler_oil" in gen_p.columns:
            heat = hor(gen_p.loc[:, ["heat_boiler_oil"]])
        if "heat_boiler_gas" in gen_p.columns:
            heat = hor(gen_p.loc[:, ["heat_boiler_gas"]])
        heat = hor(heat, abs(link_p_out.loc[:, "heat_pump"]))
        heat = heat.cumsum(axis=1)
        heat = hor(heat, store_p.loc[:, "heat_storage"])
        heat = hor(heat, demand_df.loc[:, "heat_demand"])

        # line_type = ["-", "--", ":", "<", "o"]
        color = ["b-", "g--", "r:", "m*", "k+"]
        # heat graph
        # hourly
        for i in range(len(heat.columns)):
            plt.plot(heat.index, heat.loc[:, heat.columns[i]], color[i], label=heat.columns[i])

        if not path.join(output_folder, "vis"):
            os.mkdir(path.join(output_folder, "vis"))
        if not path.isdir(output_folder, "vis", folder_name):
            os.mkdir(path.join(output_folder, "vis", folder_name)

        plot_con("heat_energy", "time in hours", "energy in MWh", path.join(output_folder, "vis", folder_name))

        # heat = hor(heat, store_e.loc[:, "heat_storage"])
        # plt.plot(heat.index, store_e.loc[:, "heat_storage"], color[0], label="demand")
