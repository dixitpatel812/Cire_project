import numpy as np
import pypsa
from os import path, mkdir
import pandas as pd
import matplotlib.pyplot as plt
import mopy as mo


results_folder_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/"
#########################
folder = "r_0.2" + "/"
#########################
results_folder = path.join(results_folder_path, folder)
vis_folder = path.join(results_folder, "vis/")
ind_folder = path.join(vis_folder,  "ind/")
opt_folder = path.join(vis_folder,  "opt/")
total_folder = path.join(vis_folder,  "total/")
pie_folder = path.join(vis_folder,  "pie/")

#create folders
if not path.isdir(vis_folder):
    mkdir(vis_folder)
if not path.isdir(ind_folder):
    mkdir(ind_folder)
if not path.isdir(opt_folder):
    mkdir(opt_folder)
if not path.isdir(total_folder):
    mkdir(total_folder)
if not path.isdir(pie_folder):
    mkdir(pie_folder)

#read files
total_energy = pd.read_csv(path.join(results_folder, "total_energy.csv"), index_col="tech")
max_energy = pd.read_csv(path.join(results_folder, "max_energy.csv"), index_col="tech")
opt = pd.read_csv(path.join(results_folder, "opt.csv"), index_col="tech")

opt = opt.iloc[[0, 1, 2], : ]
opt = mo.ver(opt, max_energy.iloc[3:, :])


opt.to_csv(path.join(vis_folder, "opt.csv"))

p = opt.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 19, 22], :]

########################additional dataframes#####################
opt_re = opt.loc[["solar", "wind_offshore", "wind_onshore"], :]
opt_link = opt.loc[[ "electrolyser", "heat_pump"], :]

electron_p_re = opt.loc[["solar", "wind_offshore", "wind_onshore", "biomass", "hydropower"], :]
electron_p_nre = opt.loc[["lignite_coal", "hard_coal", "natural_gas", "oil"], :]
electron_c = opt.loc[["battery_charging", "hydro_charging", "electrolyser", "heat_pump"], :]

heat_energy = opt.loc[["heat_pump", "heat_boiler_oil", "heat_boiler_gas", "heat_charging"], :]
heat_energy.loc["heat_pump", :] = heat_energy.loc["heat_pump", :] * 1.84

hydrogen_energy = opt.loc[["electrolyser", "steam_reforming", "hydrogen_charging"], :]
hydrogen_energy.loc["electrolyser", :] = hydrogen_energy.loc["electrolyser", :] * .71
########################additional dataframes#####################


#################line_graph###################
mo.vis_all(electron_p_re, "RE_generation", vis_folder)
mo.vis_all(electron_p_nre, "NRE_generation", vis_folder)
mo.vis_all(electron_c, "Electricity_consumption", vis_folder)
mo.vis_all(hydrogen_energy, "Hydrogen_energy", vis_folder)
mo.vis_all(heat_energy, "Heat_energy", vis_folder)
mo.vis_all(total_energy, "total_energy", vis_folder)

mo.vis_all(opt_re, "RE_opt", opt_folder)
mo.vis_ind(opt, "opt", opt_folder)

mo.vis_ind(heat_energy, "Heat", ind_folder)
mo.vis_ind(total_energy, "Total", total_folder)

for i in p.columns:
    plt.pie(p.loc[:, i], labels=p.index, autopct="%1.1f%%")
    plt.title(i)
    plt.savefig(path.join(pie_folder, i + ".png"))
    plt.clf()

####################################Folders######################################

