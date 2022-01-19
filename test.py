import pandas as pd
from os import path
from numpy import nan as nan
import matplotlib.pyplot as plt

import mopy
from mopy import time_division as td
color = ["b-", "g--", "k:", "m<", "k+"]

output_folder = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/old_0/"
input_folder = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/old_0.1/"
profile_df = pd.read_csv(path.join(input_folder, "generators-p_max_pu.csv"), index_col="name", parse_dates=True)
demand_df = pd.read_csv(path.join(input_folder, "loads-p_set.csv"), index_col="name", parse_dates=True)

vis_folder = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/input_folder/vis/"

# print(profile_df)

# profile
# hourly
# solar
# plt.plot(profile_df.index, profile_df.loc[:, "solar"], color[0], label="solar")
# wind_off
# plt.plot(profile_df.index, profile_df.loc[:, "wind_offshore"], color[1], label="wind_off")
# wind_on
# plt.plot(profile_df.index, profile_df.loc[:, "wind_onshore"], color[2], label="wind_on")

# daily
profile_d = td(profile_df, 24)
# solar
# plt.plot(profile_d.index, profile_d.loc[:, "solar"], color[0], label="solar")
# wind_off
plt.plot(profile_d.index, profile_d.loc[:, "wind_offshore"], color[1], label="wind_off")
# wind_on
plt.plot(profile_d.index, profile_d.loc[:, "wind_onshore"], color[2], label="wind_on")


title = "Wind profiles daily"
# plt.xticks(data_frame.columns, rotation="vertical")
plt.title(title)
plt.xlabel("Time in days")
plt.ylabel("factor")
plt.legend()
# plt.show()
plt.savefig(path.join(vis_folder, title + ".png"), dpi=600)
plt.clf()



# load
# hourly
# print(demand_df)
# plt.plot(demand_df.index, demand_df.loc[:, "electricity_demand"], color[0], label="electricity")
# plt.plot(demand_df.index, demand_df.loc[:, "heat_demand"], color[1], label="heat")

# daily
# demand_df_d = td(demand_df, 24)

# print(demand_df_d)
# plt.plot(demand_df_d.index, demand_df_d.loc[:, "electricity_demand"], color[0], label="electricity")
# plt.plot(demand_df_d.index, demand_df_d.loc[:, "heat_demand"], color[1], label="heat")






# folder
# folder_name = "0"
# folder_path = path.join(output_folder, folder_name)
# gen_p = pd.read_csv(path.join(folder_path, "generators-p.csv"), index_col="name", parse_dates=True)
# link_p1= pd.read_csv(path.join(folder_path, "links-p1.csv"), index_col="name", parse_dates=True)
# store_e = pd.read_csv(path.join(folder_path, "stores-e.csv"), index_col="name", parse_dates=True)
#
# heat = pd.DataFrame(index=demand_df.index)
# heat = mopy.hor(gen_p.loc[:, ["heat_boiler_oil", "heat_boiler_gas"]], abs(link_p1.loc[:, "heat_pump"]))
# heat = mopy.hor(heat, store_e.loc[:, "heat_storage"])
# print(heat.head(50))
# heat = heat.cumsum(axis=1)
# print(heat.head(50))


# heat graph
# hourly
# for i in heat.columns:
#     plt.plot(heat.index, heat.loc[:, i], label=i)
# plt.plot(heat.index, demand_df.loc[:, "heat_demand"], label="demand")


# daily
# heat_d = td(heat, 24*4)
# demand_df_d = td(demand_df, 24*4)
# for i in heat_d.columns:
#     plt.plot(heat_d.index, heat_d.loc[:, i], label=i)
# plt.plot(heat_d.index, demand_df_d.loc[:, "heat_demand"], label="demand")

# title = ""
# # plt.xticks(data_frame.columns, rotation="vertical")
# plt.title(title)
# plt.xlabel("time")
# plt.ylabel("MWh")
# plt.legend()
# plt.show()
# # plt.savefig(path.join(folder_path, title + ".png"))
# plt.clf()



