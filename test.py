import numpy as np
import pypsa
import os
import pandas as pd
import matplotlib.pyplot as plt
import mopy as mo
import math

###read data
file_path = "/run/media/dixit/D8_HD/D/Study/SEM_2/Cire/moosces/demand_data/"
file_name = "2030_time_series.csv"
data = pd.read_csv(os.path.join(file_path, file_name), index_col="time", parse_dates=True)

cost = pd.DataFrame()

#########################
min_emission = 158668874
results_folder_path = "/run/media/dixit/D8_HD/D/Study/SEM_2/Cire/moosces/output_folder/test_six_two/"
#########################

###generator["p_nom", "marginal_cost", "efficiency", "capital_cost", "p_nom_max"]
gen_solar = mo.gen_data(130000, 0, 1, 550000, 170000)
gen_wind_off = mo.gen_data(28000, 0, 1, 1100000, 50000)
gen_wind_on = mo.gen_data(102000, 0, 1, 2100000, 122000)
gen_biomass = mo.gen_data(8200, 75.8, 0.4, 2200000, 8200)
gen_hydro = mo.gen_data(4800, 0, .88, 2200000, 4800)
gen_lignite = mo.gen_data(9000, 44.9, 0.485, 2200000, 9000)
gen_hard_coal = mo.gen_data(15000, 59.6, 0.51, 2200000, 15000)
gen_natural_gas = mo.gen_data(66000, 68.1, 0.62, 2200000, 66000)
gen_oil = mo.gen_data(1000, 163.3, 0.3, 2200000, 1000)

gen_steam_reforming = mo.gen_data(2250, 50.8, 0.83, 300000, 3000)

gen_boi_oil = mo.gen_data(13000, 57.6, .85, 457000, 15100)
gen_boi_gas = mo.gen_data(58000, 44.9, .94, 387000, 65200)

##### assumptions
# gen_boi_oil = mo.gen_data(15000, 53.8, 0.91, 7, 15000)
# gen_boi_gas = mo.gen_data(80000, 45.9, 0.92, 2, "inf")


###here efficincyies are considred as sqrt(actual efficiency)
###store["e_nom", "marginal_cost", "standing_loss", "capital_cost", "e_nom_max", "efficiency"]
store_battery = mo.sto_data(122.2, 0, .007, 950000, 15000, math.sqrt(.98))
store_hydro = mo.sto_data(11000, 0, 0, 3000000, 14000, math.sqrt(.8))

store_hydrogen = mo.sto_data(1000, 0, 0, 310000, 5000, math.sqrt(.40))

store_heat = mo.sto_data(3000, 0, 0.001, 55000, 20000, math.sqrt(.98))


###link["p_nom", "marginal_cost", "efficiency", "capital_cost", "p_nom_max"]

link_bat_c = mo.link_data(0, 0, store_battery["efficiency"], 0, store_battery["e_nom_max"] / store_battery["efficiency"])
link_bat_d = mo.link_data(0, 0, store_battery["efficiency"], 0, store_battery["e_nom_max"] / store_battery["efficiency"])

link_hydro_c = mo.link_data(0, 0, store_hydro["efficiency"], 0, store_hydro["e_nom_max"] / store_hydro["efficiency"])
link_hydro_d = mo.link_data(0, 0, store_hydro["efficiency"], 0, store_hydro["e_nom_max"] / store_hydro["efficiency"])

link_h2_c = mo.link_data(0, 0, store_hydrogen["efficiency"], 0, store_hydrogen["e_nom_max"] / store_hydrogen["efficiency"])
link_h2_d = mo.link_data(0, 0, store_hydrogen["efficiency"], 0, store_hydrogen["e_nom_max"] / store_hydrogen["efficiency"])

link_ele = mo.link_data(5000, 15.2, .71, 1137000, 15000)
link_h2e = mo.link_data(500, 0.0, .8, 1000000, 1000)

link_heat_c = mo.link_data(0, 0, store_heat["efficiency"], 0, store_heat["e_nom_max"] / store_heat["efficiency"])
link_heat_d = mo.link_data(0, 0, store_heat["efficiency"], 0, store_heat["e_nom_max"] / store_heat["efficiency"])

link_heat_pump = mo.link_data(32000, 0.0, 1.84, 2161000, 105000)

#####################################################################################

### Carrier with CO2 emissions
carrier = {"gas":0.20,"hard_coal":0.34,"lignite":0.40,"oil":0.28}


###network
n = pypsa.Network()
n.set_snapshots(data.index)


###Carriers
n.add("Carrier", "Gas", co2_emissions=carrier["gas"])
n.add("Carrier", "Hard_coal", co2_emissions=carrier["hard_coal"])
n.add("Carrier", "Lignite", co2_emissions=carrier["lignite"])
n.add("Carrier", "Oil", co2_emissions=carrier["oil"])


###electricity
n.add("Bus", "electricity")

n.add("Generator", "solar", p_nom=gen_solar["p_nom"], bus="electricity", marginal_cost=gen_solar["marginal_cost"], p_nom_extendable=True, p_nom_max=gen_solar["p_nom_max"],
      p_max_pu=data['solar_profile'], efficiency=gen_solar["efficiency"], capital_cost=gen_solar["capital_cost"])
n.add("Generator", "wind_offshore", p_nom=gen_wind_off["p_nom"], bus="electricity", marginal_cost=gen_wind_off["marginal_cost"], p_nom_extendable=True,
      p_nom_max=gen_wind_off["p_nom_max"], p_max_pu=data['wind_offshore_profile'], efficiency=gen_wind_off["efficiency"], capital_cost=gen_wind_off["capital_cost"])
n.add("Generator", "wind_onshore", p_nom=gen_wind_on["p_nom"], bus="electricity", marginal_cost=gen_wind_on["marginal_cost"], p_nom_extendable=True,
      p_nom_max=gen_wind_on["p_nom_max"], p_max_pu=data['wind_onshore_profile'], efficiency=gen_wind_on["efficiency"], capital_cost=gen_wind_on["capital_cost"])
n.add("Generator", "biomass", p_nom=gen_biomass["p_nom"], bus="electricity", marginal_cost=gen_biomass["marginal_cost"], p_nom_extendable=True, efficiency=gen_biomass["efficiency"], capital_cost=gen_biomass["capital_cost"], p_nom_max=gen_biomass["p_nom_max"])
n.add("Generator", "hydropower", p_nom=gen_hydro["p_nom"], bus="electricity", marginal_cost=gen_hydro["marginal_cost"], p_nom_extendable=True, capital_cost=gen_hydro["capital_cost"], p_nom_max=gen_hydro["p_nom_max"],
      efficiency=gen_hydro["efficiency"])
n.add("Generator", "lignite_coal", p_nom=gen_lignite["p_nom"], bus="electricity", marginal_cost=gen_lignite["marginal_cost"], carrier="Lignite", capital_cost=gen_lignite["capital_cost"], p_nom_max=gen_lignite["p_nom_max"],
      p_nom_extendable=True, efficiency=gen_lignite["efficiency"])
n.add("Generator", "hard_coal", p_nom=gen_hard_coal["p_nom"], bus="electricity", marginal_cost=gen_hard_coal["marginal_cost"], carrier="Hard_coal", capital_cost=gen_hard_coal["capital_cost"], p_nom_max=gen_hard_coal["p_nom_max"],
      p_nom_extendable=True, efficiency=gen_hard_coal["efficiency"])
n.add("Generator", "natural_gas", p_nom=gen_natural_gas["p_nom"], bus="electricity", marginal_cost=gen_natural_gas["marginal_cost"], carrier="Gas", capital_cost=gen_natural_gas["capital_cost"], p_nom_max=gen_natural_gas["p_nom_max"],
      p_nom_extendable=True, efficiency=gen_natural_gas["efficiency"])
n.add("Generator", "oil", p_nom=gen_oil["p_nom"], bus="electricity", marginal_cost=gen_oil["marginal_cost"], carrier="Oil", p_nom_extendable=True, capital_cost=gen_oil["capital_cost"], p_nom_max=gen_oil["p_nom_max"],
      efficiency=gen_oil["efficiency"])

n.add("Load", "electricity_demand", bus="electricity", p_set=data["elec_demand"])


### battery storage
n.add("Bus", "battery_store")

n.add("Link", "battery_charging", bus0="electricity", bus1="battery_store", p_nom=link_bat_c["p_nom"], efficiency=link_bat_c["efficiency"],
      p_nom_extendable=True, marginal_cost=link_bat_c["marginal_cost"], p_nom_max=link_bat_c["p_nom_max"], capital_cost=link_bat_c["capital_cost"])
n.add("Store", "battery_storage", bus="battery_store", e_cyclic=False, e_nom=store_battery["e_nom"], e_nom_extendable=True, marginal_cost=store_battery["marginal_cost"],
      capital_cost=store_battery["capital_cost"], standing_loss=store_battery["standing_loss"], e_nom_max=store_battery["e_nom_max"])
n.add("Link", "battery_discharging", bus0="battery_store", bus1="electricity", p_nom=link_bat_d["p_nom"], efficiency=link_bat_d["efficiency"],
      p_nom_extendable=True, marginal_cost=link_bat_d["marginal_cost"], p_nom_max=link_bat_d["p_nom_max"], capital_cost=link_bat_d["capital_cost"])

### hydro storage
n.add("Bus", "hydro_store")

n.add("Link", "hydro_charging", bus0="electricity", bus1="hydro_store", p_nom=link_hydro_c["p_nom"], efficiency=link_hydro_c["efficiency"],
      p_nom_extendable=True, marginal_cost=link_hydro_c["marginal_cost"], p_nom_max=link_hydro_c["p_nom_max"], capital_cost=link_hydro_c["capital_cost"])
n.add("Store", "hydro_storage", bus="hydro_store", e_cyclic=False, e_nom=store_hydro["e_nom"], e_nom_extendable=True, marginal_cost=store_hydro["marginal_cost"],
      capital_cost=store_hydro["capital_cost"], standing_loss=store_hydro["standing_loss"], e_nom_max=store_hydro["e_nom_max"])
n.add("Link", "hydro_discharging", bus0="hydro_store", bus1="electricity", p_nom=link_hydro_d["p_nom"], efficiency=link_hydro_d["efficiency"],
      p_nom_extendable=True, marginal_cost=link_hydro_d["marginal_cost"], p_nom_max=link_hydro_d["p_nom_max"], capital_cost=link_hydro_d["capital_cost"])


###hydrogen
n.add("Bus", "hydrogen")

n.add("Generator", "steam_reforming", p_nom=gen_steam_reforming["p_nom"], bus="hydrogen", marginal_cost=gen_steam_reforming["marginal_cost"], carrier="Gas",
      p_nom_extendable=True, efficiency=gen_steam_reforming["efficiency"], capital_cost=gen_steam_reforming["capital_cost"], p_nom_max=gen_steam_reforming["p_nom_max"])

n.add("Load", "hydrogen_demand", bus="hydrogen", p_set=3652)

n.add("Link", "electrolyser", bus0="electricity", bus1="hydrogen", p_nom=link_ele["p_nom"], p_nom_max=link_ele["p_nom_max"], efficiency=link_ele["efficiency"],
      p_nom_extendable=True, marginal_cost=link_ele["marginal_cost"], capital_cost=link_ele["capital_cost"])


### hydrogen storage
n.add("Bus", "hydrogen_store")

n.add("Link", "hydrogen_charging", bus0="hydrogen", bus1="hydrogen_store", p_nom=link_h2_c["p_nom"], efficiency=link_h2_c["efficiency"],
      p_nom_extendable=True, marginal_cost=link_h2_c["marginal_cost"], p_nom_max=link_h2_c["p_nom_max"], capital_cost=link_h2_c["capital_cost"])
n.add("Store", "hydrogen_storage", bus="hydrogen_store", e_cyclic=False,  e_nom = store_hydrogen["e_nom"], e_nom_extendable=True, marginal_cost=store_hydrogen["marginal_cost"],
      capital_cost=store_hydrogen["capital_cost"], standing_loss=store_hydrogen["standing_loss"], e_nom_max=store_hydrogen["e_nom_max"])
n.add("Link", "hydrogen_discharging", bus0="hydrogen_store", bus1="hydrogen", p_nom=link_h2_d["p_nom"], efficiency=link_h2_d["efficiency"],
      p_nom_extendable=True, marginal_cost=link_h2_d["marginal_cost"], p_nom_max=link_h2_d["p_nom_max"], capital_cost=link_h2_d["capital_cost"])

n.add("Link", "hydrogen_to_electricity", bus0="hydrogen", bus1="electricity", p_nom=link_h2e["p_nom"], efficiency=link_h2e["efficiency"],
      p_nom_extendable=True, marginal_cost=link_h2e["marginal_cost"], p_nom_max=link_h2e["p_nom_max"], capital_cost=link_h2e["capital_cost"])

###heat
n.add("Bus", "heat")

n.add("Generator", "heat_boiler_oil", p_nom=gen_boi_oil["p_nom"], bus="heat", marginal_cost=gen_boi_oil["marginal_cost"], carrier="Oil",
      p_nom_extendable=True, efficiency=gen_boi_oil["efficiency"], capital_cost=gen_boi_oil["capital_cost"], p_nom_max=gen_boi_oil["p_nom_max"])
n.add("Generator", "heat_boiler_gas", p_nom=gen_boi_gas["p_nom"], bus="heat", marginal_cost=gen_boi_gas["marginal_cost"], carrier="Gas",
      p_nom_extendable=True, efficiency=gen_boi_gas["efficiency"], capital_cost=gen_boi_gas["capital_cost"], p_nom_max=gen_boi_gas["p_nom_max"])

n.add("Load", "heat_demand", bus="heat", p_set=data["heat_demand"])

n.add("Link", "heat_pump", bus0="electricity", bus1="heat", marginal_cost=link_heat_pump["marginal_cost"], p_nom=link_heat_pump["p_nom"], efficiency=link_heat_pump["efficiency"], p_nom_extendable=True, p_nom_max = link_heat_pump["p_nom_max"], capital_cost=link_heat_pump["capital_cost"])


### heat storage
n.add("Bus", "heat_store")
n.add("Link", "heat_charging", bus0="heat", bus1="heat_store", p_nom=link_heat_c["p_nom"], efficiency=link_heat_c["efficiency"],
      p_nom_extendable=True, marginal_cost=link_heat_c["marginal_cost"], p_nom_max=link_heat_c["p_nom_max"], capital_cost=link_heat_c["capital_cost"])
n.add("Store", "heat_storage", bus="heat_store", e_cyclic=False, e_nom=store_heat["e_nom"], e_nom_extendable=True, marginal_cost=store_heat["marginal_cost"],
      capital_cost=store_heat["capital_cost"], standing_loss=store_heat["standing_loss"], e_nom_max=store_heat["e_nom_max"])
n.add("Link", "heat_discharging", bus0="heat_store", bus1="heat", p_nom=link_heat_d["p_nom"], efficiency=link_heat_d["efficiency"],
      p_nom_extendable=True, marginal_cost=link_heat_d["marginal_cost"], p_nom_max=link_heat_d["p_nom_max"], capital_cost=link_heat_d["capital_cost"])



### support generatores
n.add("Generator", "support_gen_ele", p_nom=0, bus="electricity", marginal_cost=152366555000, p_nom_extendable=True,
      efficiency=0.1597 , capital_cost=50021510000000)

n.add("Generator", "support_gen_heat", p_nom=00, bus="heat", marginal_cost=152366555000, p_nom_extendable=True,
      capital_cost = 50021510000000, efficiency=0.1597)

n.add("Generator", "support_gen_hydrogen", p_nom=00, bus="hydrogen", marginal_cost=152366555000, p_nom_extendable=True,
      capital_cost = 50021510000000, efficiency=0.1597)



max_emission = 8760 * (gen_steam_reforming["p_nom"]*carrier["gas"]/gen_steam_reforming["efficiency"] +
                       gen_natural_gas["p_nom"]*carrier["gas"]/gen_natural_gas["efficiency"] +
                       gen_boi_gas["p_nom"]*carrier["gas"]/gen_boi_gas["efficiency"] +
                       gen_oil["p_nom"]*carrier["oil"]/gen_oil["efficiency"] +
                       gen_boi_oil["p_nom"]*carrier["oil"]/gen_oil["efficiency"] +
                       gen_hard_coal["p_nom"]*carrier["hard_coal"]/gen_hard_coal["efficiency"] +
                       gen_lignite["p_nom"]*carrier["lignite"]/gen_lignite["efficiency"])
# i = 166441431
i = 150000000
#110000000
# i = max_emission



i_i = i
# i = 100000000
# print(max_emission)
dif = 8000000



while i > 50000000:
    # Global constrains
    n.add("GlobalConstraint", "Co2_limit", type="primary_energy", carrier_attribute="co2_emissions", constant=i,
          sense="==")

    folder = str(int(i))

    results_folder = os.path.join(results_folder_path, folder)

    n.lopf(n.snapshots, solver_name="gurobi_direct", pyomo=False)
    n.export_to_csv_folder(results_folder)

    # print(n.generators)

    n.mremove("GlobalConstraint", ["Co2_limit"])


    #vis####################################################################################################

    #######total energy#######
    sums = pd.DataFrame()

    sums = mo.ver(sums, n.generators_t.p.sum(axis=0), n.links_t.p0.sum(axis=0))
    sums.columns = [str(round(int(i)/10e5,3)) + "M"]

    if i == i_i:
        total_energy = sums
    else:
        total_energy = mo.hor(total_energy, sums)
    #######total energy#######


    #######p_nom_opt#######
    optimal = pd.DataFrame()

    optimal =  mo.ver(optimal, n.generators.loc[:, "p_nom_opt"], n.links.loc[:,"p_nom_opt"], n.stores.loc[:,"e_nom_opt"])
    optimal.columns = [str(round(int(i)/10e5,3)) + "M"]

    if i == i_i:
        opt = optimal
    else:
        opt = mo.hor(opt, optimal)
    ########p_nom_opt######

    #vis####################################################################################################



    #cost####################################################################################################

    ###gen###
    for j in n.generators_t.p.columns:
        if n.generators.loc[j, "p_nom_opt"] - n.generators.loc[j, "p_nom"] > 0:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = n.generators.loc[j, "capital_cost"] * (n.generators.loc[j, "p_nom_opt"] - n.generators.loc[j, "p_nom"])
        else:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = 0

    ###links###
    for j in n.links_t.p0.columns:
        if n.links.loc[j, "p_nom_opt"] - n.links.loc[j, "p_nom"] > 0:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = n.links.loc[j, "capital_cost"] * (n.links.loc[j, "p_nom_opt"] - n.links.loc[j, "p_nom"])
        else:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = 0

    ###stores###
    for j in n.stores_t.p.columns:
        if n.stores.loc[j, "e_nom_opt"] - n.stores.loc[j, "e_nom"] > 0:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = n.stores.loc[j, "capital_cost"] * (n.stores.loc[j, "e_nom_opt"] - n.stores.loc[j, "e_nom"])
        else:
            cost.loc[j, str(round(int(i)/10e5,3)) + "M"] = 0


    #cost####################################################################################################

    if n.generators.loc["support_gen_ele", "p_nom_opt"] != 0 or n.generators.loc[
        "support_gen_heat", "p_nom_opt"] != 0 or n.generators.loc["support_gen_hydrogen", "p_nom_opt"] != 0:
        print("Error support_gen")
        i = 0


    i = int(i) - dif
    total_energy.index.name = "tech"
    opt.index.name = "tech"
    cost.index.name = "tech"
    total_energy.to_csv(os.path.join(results_folder_path, "total_energy.csv"))
    opt.to_csv(os.path.join(results_folder_path, "opt.csv"))
    cost.to_csv(os.path.join(results_folder_path, "cost.csv"))
    total_cost = cost.sum(axis=0)
    total_cost.to_csv(os.path.join(results_folder_path, "total_cost.csv"))
    # break


