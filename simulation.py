import mopy
import pypsa_output
import d8_output
import vis

# # mopy
input_data_folder_name = "fi_4.0.1"
s_limit = 60
difference = 5


# mopy.folder_exist_err(mopy.input_path, input_data_folder_name, exist=False)


# # pypsa_output
# pypsa_output.output(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)

# # d8_output
# d8_output.curtailment(input_data_folder_name, start_limit=s_limit, reduction=difference, end_limit=0)

# # vis
# vis.stacked_energy_column_graph(input_data_folder_name)
# vis.vis(input_data_folder_name, curl=True, cost=True)
# vis.vis_comparison_ind(input_data_folder_name, vis.comparison_list)
# # line graph
# vis.energy_line_graph(input_data_folder_name, "electricity_total.csv")
# vis.energy_line_graph(input_data_folder_name, "heat_total.csv")
# vis.energy_line_graph(input_data_folder_name, "hydrogen_total.csv")
# vis.curtailment_bar_graph(input_data_folder_name)