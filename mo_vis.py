import numpy as np
import pypsa
from os import path, mkdir
import pandas as pd
import matplotlib.pyplot as plt
import mopy as mo


results_folder_path = "/run/media/d8/D8_HD/D/Sem_3/Cire/moosces/output_folder/"
#########################
folder = "old_0" + "/"
#########################
results_folder = path.join(results_folder_path, folder)
vis_folder = path.join(results_folder, "vis/")
ind_folder = path.join(vis_folder,  "ind/")
opt_folder = path.join(vis_folder,  "opt/")

#create folders
if not path.isdir(vis_folder):
    mkdir(vis_folder)
if not path.isdir(ind_folder):
    mkdir(ind_folder)
if not path.isdir(opt_folder):
    mkdir(opt_folder)

#read files
total_energy = pd.read_csv(path.join(results_folder, "total_energy.csv"), index_col="tech")
opt = pd.read_csv(path.join(results_folder, "opt.csv"), index_col="tech")
opt = opt.iloc[[0, 1, 2, 10, 11, 12, -14, -13, -10, -9, -8, -7, -6, -5, -4, -2, -1], : ]
opt.to_csv(path.join(vis_folder, "opt.csv"))

########################additional dataframes#####################
opt_re = opt.loc[["solar", "wind_offshore", "wind_onshore"], :]
opt_link = opt.loc[[ "electrolyser", "heat_pump"], :]

electron_p_re = total_energy.loc[["solar", "wind_offshore", "wind_onshore", "biomass", "hydropower"], :]
electron_p_nre = total_energy.loc[["lignite_coal", "hard_coal", "natural_gas", "oil"], :]
electron_c = total_energy.loc[["battery_charging", "hydro_charging", "electrolyser", "heat_pump"], :]

heat_energy = total_energy.loc[["heat_pump", "heat_boiler_oil", "heat_boiler_gas", "heat_charging"], :]
heat_energy.loc["heat_pump", :] = heat_energy.loc["heat_pump", :] * 1.84

hydrogen_energy = total_energy.loc[["electrolyser", "steam_reforming", "hydrogen_charging"], :]
hydrogen_energy.loc["electrolyser", :] = hydrogen_energy.loc["electrolyser", :] * .71
########################additional dataframes#####################


#################line_graph###################
mo.vis_all(electron_p_re, "RE_generation", vis_folder)
mo.vis_all(electron_p_nre, "NRE_generation", vis_folder)
mo.vis_all(electron_c, "Electricity_consumption", vis_folder)
mo.vis_all(hydrogen_energy, "Hydrogen_energy", vis_folder)
mo.vis_all(heat_energy, "Heat_energy", vis_folder)

mo.vis_all(opt_re, "RE_opt", opt_folder)
mo.vis_ind(opt_link, "opt", opt_folder)

mo.vis_ind(heat_energy, "Heat", ind_folder)