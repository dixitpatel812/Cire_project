import mopy
import pypsa_output
import d8_output
import vis

# # mopy
input_data_folder_name = "final_0"
s_limit = 180
difference = 90
# # # #
comparison_list = ["electrolyser", "solar", "natural_gas", "lignite_coal", "hard_coal", "wind_onshore", "wind_offshore", 'heat_pump']
# # #
# mopy.folder_exist_err(mopy.input_path, input_data_folder_name, exist=False)
# # #
# # #
# # # # pypsa_output
# # x = pypsa_output.output(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0, GC=False, ones=True)
# # print(x)
# pypsa_output.output(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)
#
# # # d8_output
# d8_output.curtailment(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)
# d8_output.store_cycle(input_data_folder_name)
# #
#
#
# # # vis
# vis.vis(input_data_folder_name, curl=True)
# vis.vis(input_data_folder_name, cost=True)
# vis.vis(input_data_folder_name, stacked_energy_column_graph=True)
# vis.vis_comparison_ind(input_data_folder_name,  c_list=comparison_list)
# # # line graph
# vis.vis(input_data_folder_name, opt_lines=True)
vis.vis(input_data_folder_name, energy_lines=True)
# vis.cycle_bar_graph(input_data_folder_name)