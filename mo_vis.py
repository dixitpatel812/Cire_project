import numpy as np
import pypsa
import os
import pandas as pd
import matplotlib.pyplot as plt
import mopy as mo

#########################
results_folder_path = "/run/media/dixit/D8_HD/D/Study/SEM_2/Cire/moosces/output_folder/present/"
#########################

total_energy = pd.read_csv(os.path.join(results_folder_path, "total_energy.csv"), index_col = "tech")


#######read file + vis
electron_p = total_energy.loc[["solar", "wind_offshore", "wind_onshore", "biomass", "hydropower", "lignite_coal", "hard_coal", "natural_gas", "oil"],:]
electron_c = total_energy.loc[["battery_charging", "hydro_charging", "electrolyser", "heat_pump", "hydrogen_to_electricity"],:]
electron_c.loc["hydrogen_to_electricity", :] = electron_c.loc["hydrogen_to_electricity", :] * .8

heat_energy = total_energy.loc[["heat_pump", "heat_boiler_oil", "heat_boiler_gas", "heat_charging"],:]
heat_energy.loc["heat_pump", :] = heat_energy.loc["heat_pump", :] * 1.84

hydrogen_energy = total_energy.loc[["electrolyser", "steam_reforming", "hydrogen_charging"],:]
hydrogen_energy.loc["electrolyser", :] = hydrogen_energy.loc["electrolyser", :] * .71

########################Electricity_generation##################################
# #####individual######
# for i in electron_p.index:
#     plt.plot(electron_p.columns, electron_p.loc[i, :], label=i)
#     plt.title(i)
#     plt.xlabel("CO2_emission limit")
#     plt.ylabel("MWh")
#     plt.xticks(electron_p.columns, rotation="vertical")
#     plt.subplots_adjust(bottom=.17)
#     # plt.savefig(os.path.join(results_folder_path, i + ".png"), dpi = 1200)
#     plt.savefig(os.path.join(results_folder_path, i + ".png"))
#     plt.clf()
# #####individual######
#
# #####all in one######
# for i in electron_p.index:
#     plt.plot(electron_p.columns, electron_p.loc[i, :], label=i)
#
# plt.xticks(electron_p.columns, rotation="vertical")
# plt.title("Electricity_generation")
# plt.xlabel("CO2_emission limit")
# plt.ylabel("MWh")
# plt.legend()
# plt.subplots_adjust(bottom=.17)
# # plt.savefig(os.path.join(results_folder_path, "electricity_generation.png"), dpi = 1200)
# plt.savefig(os.path.join(results_folder_path, "electricity_generation.png"))
# plt.clf()
# ####all in one######
#
# #########################Electricity_generation##################################
#
#
#
#
# #########################Electricity_consumption##################################
#
# #####individual######
# for i in electron_c.index:
#     plt.plot(electron_c.columns, electron_c.loc[i, :], label=i)
#     plt.title(i)
#     plt.xlabel("CO2_emission limit")
#     plt.ylabel("MWh")
#     plt.xticks(electron_c.columns, rotation="vertical")
#     plt.subplots_adjust(bottom=.17)
#     # plt.savefig(os.path.join(results_folder_path, i + ".png"), dpi = 1200)
#     plt.savefig(os.path.join(results_folder_path, i + ".png"))
#     plt.clf()
#     # break
#
# #####individual######
#
#
# ####all in one######
# for i in electron_c.index:
#     plt.plot(electron_c.columns, electron_c.loc[i, :], label=i)
#
# plt.xticks(electron_c.columns, rotation="vertical")
# plt.title("Electricity_consumption")
# plt.xlabel("CO2_emission limit")
# plt.ylabel("MWh")
# plt.legend()
# plt.subplots_adjust(bottom=.17)
# # plt.savefig(os.path.join(results_folder_path, "electricity_consumption.png"), dpi = 1200)
# plt.savefig(os.path.join(results_folder_path, "electricity_consumption.png"))
# plt.clf()
# ####all in one######

#########################Electricity_consumption##################################


########################Hydrogen##################################
#####individual######
# for i in hydrogen_energy.index:
#     plt.plot(hydrogen_energy.columns, hydrogen_energy.loc[i, :], label=i)
#     plt.title(i)
#     plt.xlabel("CO2_emission limit")
#     plt.ylabel("MWh")
#     plt.xticks(hydrogen_energy.columns, rotation="vertical")
#     plt.subplots_adjust(bottom=.17)
#     # plt.savefig(os.path.join(results_folder_path, i + ".png"), dpi = 1200)
#     plt.savefig(os.path.join(results_folder_path, i + ".png"))
#     plt.clf()
# #####individual######
#
# #####all in one######
# for i in hydrogen_energy.index:
#     plt.plot(hydrogen_energy.columns, hydrogen_energy.loc[i, :], label=i)
#
# plt.xticks(hydrogen_energy.columns, rotation="vertical")
# plt.title("Hydrogen_Energy")
# plt.xlabel("CO2_emission limit")
# plt.ylabel("MWh")
# plt.legend()
# plt.subplots_adjust(bottom=.17)
# # plt.savefig(os.path.join(results_folder_path, "electricity_generation.png"), dpi = 1200)
# plt.savefig(os.path.join(results_folder_path, "hydrogen_energy.png"))
# plt.clf()
####all in one######

#########################Hydrogen##################################



########################Heat##################################
#####individual######
for i in heat_energy.index:
    plt.plot(heat_energy.columns, heat_energy.loc[i, :], label=i)
    plt.title(i)
    plt.xlabel("CO2_emission limit")
    plt.ylabel("MWh")
    plt.xticks(heat_energy.columns, rotation="vertical")
    plt.subplots_adjust(bottom=.17)
    # plt.savefig(os.path.join(results_folder_path, i + ".png"), dpi = 1200)
    plt.savefig(os.path.join(results_folder_path, i + ".png"))
    plt.clf()
#####individual######

#####all in one######
for i in heat_energy.index:
    plt.plot(heat_energy.columns, heat_energy.loc[i, :], label=i)

plt.xticks(heat_energy.columns, rotation="vertical")
plt.title("Heat_Energy")
plt.xlabel("CO2_emission limit")
plt.ylabel("MWh")
plt.legend()
plt.subplots_adjust(bottom=.17)
# plt.savefig(os.path.join(results_folder_path, "electricity_generation.png"), dpi = 1200)
plt.savefig(os.path.join(results_folder_path, "heat_energy.png"))
plt.clf()
####all in one######

#########################Heat##################################