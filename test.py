import numpy as np
import pypsa
import os
import pandas as pd
import matplotlib.pyplot as plt
import mopy as mo

results_folder_path = "/run/media/dixit/D8_HD/D/Study/SEM_2/Cire/moosces/output_folder/heat/36981225/"

x = pd.read_csv(os.path.join(results_folder_path, "generators-p.csv"), index_col= "time")
y = pd.read_csv(os.path.join(results_folder_path, "generators-p_max_pu.csv"), index_col= "time")


solar_gen = pd.DataFrame()
wind_offshore_gen = pd.DataFrame()
wind_onshore_gen = pd.DataFrame()


solar_gen.loc[:, "solar"] = x.solar
solar_gen.loc[:, "solar_max"] = y.solar * 170000


wind_offshore_gen.loc[:, "wind_offshore"] = x.wind_offshore
wind_offshore_gen.loc[:, "wind_offshore_max"] = y.wind_offshore * 45000


wind_onshore_gen.loc[:, "wind_onshore"] = x.wind_onshore
wind_onshore_gen.loc[:, "wind_onshore_max"] = y.wind_onshore * 135000


sp = pd.DataFrame()
sp["solar"] = solar_gen.solar_max - solar_gen.solar
sp["wind_offshore"] = wind_offshore_gen.wind_offshore_max - wind_offshore_gen.wind_offshore
sp["wind_onshore"] = wind_onshore_gen.wind_onshore_max - wind_onshore_gen.wind_onshore

print(sp.solar[sp.solar>0].sum())
print(sp.wind_offshore[sp.wind_offshore>0].sum())
print(sp.wind_onshore[sp.wind_onshore>0].sum())