import mopy
import pypsa_output
import mo_vis
import test

#perfect
input_data_folder_name = "fi_4.0"
mopy.folder_exist_err(mopy.input_path, input_data_folder_name, exist=False)

#working
pypsa_output.output(input_data_folder_name, start_limit=180, reduction=20, end_limit=0, m_factor=10e5, output_data=True, ones=False)


mo_vis.vis(input_data_folder_name, line=True)


test.curtailment(input_data_folder_name)
test.vis_new(input_data_folder_name, curl=True)