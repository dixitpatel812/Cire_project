import mopy
import pypsa_output
import d8_output
import vis

# # mopy
input_data_folder_name = "test"
s_limit = 180
difference = 180
#
comparison_list = ["electrolyser", "solar", "biomass", "natural_gas", "lignite_coal", "hard_coal", 'hydropower']
#
mopy.folder_exist_err(mopy.input_path, input_data_folder_name, exist=False)
#
#
# # pypsa_output
pypsa_output.output(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)
#
# # d8_output
d8_output.curtailment(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)
#
# # vis
vis.stacked_energy_column_graph(input_data_folder_name)
vis.vis(input_data_folder_name, curl=True, cost=True)
vis.vis_comparison_ind(input_data_folder_name,  c_list=comparison_list)
# # line graph
vis.energy_line_graph(input_data_folder_name, "electricity_total.csv")
vis.energy_line_graph(input_data_folder_name, "heat_total.csv")
vis.energy_line_graph(input_data_folder_name, "hydrogen_total.csv")