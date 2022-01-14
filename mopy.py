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
