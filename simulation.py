import mopy
import mo
import mo_vis
import test

#perfect
input_data_folder_name = "fi_4.0"
mopy.folder_exist(mopy.input_path, input_data_folder_name, exist=True)

#working
mo.cire(input_data_folder_name)


mo_vis.vis(input_data_folder_name, line=True)


test.curtailment(input_data_folder_name)
test.vis_new(input_data_folder_name, curl=True)