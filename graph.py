import pandas as pd
from os import path
from numpy import nan as nan
import matplotlib.pyplot as plt

import mopy
from mopy import time_division as td

# output_folder = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/old_0/"
# input_folder = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/old_0.1/"
# profile_df = pd.read_csv(path.join(input_folder, "generators-p_max_pu.csv"), index_col="name", parse_dates=True)
# demand_df = pd.read_csv(path.join(input_folder, "loads-p_set.csv"), index_col="name", parse_dates=True)
#
# # print(profile_df)
#
# # profile
# # hourly
# # solar
# # plt.plot(profile_df.index, profile_df.loc[:, "solar"], label="solar")
# # wind_off
# # plt.plot(profile_df.index, profile_df.loc[:, "wind_offshore"], label="wind_off")
# # wind_on
# # plt.plot(profile_df.index, profile_df.loc[:, "wind_onshore"], label="wind_on")
#
# # daily
# # profile_d = td(profile_df, 24)
# # solar
# # plt.plot(profile_d.index, profile_d.loc[:, "solar"], label="solar")
# # wind_off
# # plt.plot(profile_d.index, profile_d.loc[:, "wind_offshore"], label="wind_off")
# # wind_on
# # plt.plot(profile_d.index, profile_d.loc[:, "wind_onshore"], label="wind_on")
#
#
# # load
# # hourly
# # print(demand_df)
# # plt.plot(demand_df.index, demand_df.loc[:, "electricity_demand"], label="ele")
# # plt.plot(demand_df.index, demand_df.loc[:, "heat_demand"], label="heat")
#
# # daily
# # demand_df_d = td(demand_df, 24)
#
# # print(demand_df_d)
# # plt.plot(demand_df_d.index, demand_df_d.loc[:, "electricity_demand"], label="ele")
# # plt.plot(demand_df_d.index, demand_df_d.loc[:, "heat_demand"], label="heat")
#
#
#
#
#
# # folder
# folder_name = "180000000"
# folder_path = path.join(output_folder, folder_name)
# gen_p = pd.read_csv(path.join(folder_path, "generators-p.csv"), index_col="name", parse_dates=True)
# link_p_out = pd.read_csv(path.join(folder_path, "links-p1.csv"), index_col="name", parse_dates=True)
# link_p_in = pd.read_csv(path.join(folder_path, "links-p0.csv"), index_col="name", parse_dates=True)
# store_e = pd.read_csv(path.join(folder_path, "stores-e.csv"), index_col="name", parse_dates=True)
# store_p = pd.read_csv(path.join(folder_path, "stores-p.csv"), index_col="name", parse_dates=True)
#
# heat = pd.DataFrame(index=demand_df.index)
# if "heat_boiler_oil" in gen_p.columns:
#     heat = mopy.hor(gen_p.loc[:, ["heat_boiler_oil"]])
# if "heat_boiler_gas" in gen_p.columns:
#     heat = mopy.hor(gen_p.loc[:, ["heat_boiler_gas"]])
# heat = mopy.hor(heat, abs(link_p_out.loc[:, "heat_pump"]))
# heat = heat.cumsum(axis=1)
# heat = mopy.hor(heat, store_p.loc[:, "heat_storage"])
# heat = mopy.hor(heat, demand_df.loc[:, "heat_demand"])
#
# # line_type = ["-", "--", ":", "<", "o"]
# color = ["b-", "g--", "r:", "m*", "k+"]
# # heat graph
# # hourly
# for i in range(len(heat.columns)):
#     plt.plot(heat.index, heat.loc[:, heat.columns[i]], color[i], label=heat.columns[i])
#
# title = "heat energy"
# plt.title(title)
# plt.xlabel("time in hours")
# plt.ylabel("MWh")
# plt.legend()
# plt.show()
# plt.savefig(path.join(folder_path, title + ".png"))
# plt.clf()

# heat = mopy.hor(heat, store_e.loc[:, "heat_storage"])
# plt.plot(heat.index, store_e.loc[:, "heat_storage"], color[0],  label="demand")


mopy.graph("r0.2")