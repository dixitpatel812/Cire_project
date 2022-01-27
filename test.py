import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt


def vis_ind(data_frame, title, folder_path):
    for i in data_frame.index:
        plt.plot(data_frame.columns, data_frame.loc[i, :], label=i)
        plt.title(title + "  " + i)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("")
        plt.xticks(data_frame.columns, rotation="vertical")
        plt.subplots_adjust(bottom=.17)
        plt.savefig(mo.path.join(folder_path, title + "_" + i + ".png"))
        plt.clf()


def vis_new(data_folder_name, cost=False, cur=False, opt=False, energy=False):
    r_folder = mo.path.join(mo.output_path, data_folder_name, "results")

    if energy:
        electricity = pd.read_csv(mo.path.join(r_folder, "electricity_total.csv"), index_col=0)
        heat = pd.read_csv(mo.path.join(r_folder, "heat_total.csv"), index_col=0)
        hydrogen = pd.read_csv(mo.path.join(r_folder, "hydrogen_total.csv"), index_col=0)

        if not mo.path.isdir(mo.path.join(r_folder, "electricity_total_ind")):
            mo.mkdir(mo.path.join(r_folder, "electricity_total_ind"))
        vis_ind(abs(electricity), "electricity_total", mo.path.join(r_folder, "electricity_total_ind"))

        if not mo.path.isdir(mo.path.join(r_folder, "hydrogen_total_ind")):
            mo.mkdir(mo.path.join(r_folder, "hydrogen_total_ind"))
        vis_ind(abs(hydrogen), "hydrogen_total", mo.path.join(r_folder, "hydrogen_total_ind"))

        if not mo.path.isdir(mo.path.join(r_folder, "heat_total_ind")):
            mo.mkdir(mo.path.join(r_folder, "heat_total_ind"))
        vis_ind(abs(heat), "heat_total", mo.path.join(r_folder, "heat_total_ind"))

    if opt:
        opt_file = pd.read_csv(mo.path.join(r_folder, "opt.csv"), index_col=0)
        if not mo.path.isdir(mo.path.join(r_folder, "opt_ind")):
            mo.mkdir(mo.path.join(r_folder, "opt_ind"))
        vis_ind(opt_file, "opt", mo.path.join(r_folder, "opt_ind"))

    if cost:
        cost = pd.read_csv(mo.path.join(r_folder, "cost.csv"), index_col=0)
        plt.plot(cost.columns, cost.sum(axis=0)/1e9)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("Total costs in billion Euro")
        plt.title("Cost of reducing the CO2 emissions")
        plt.savefig(mo.path.join(r_folder, "cost.png"), dpi=600)
        plt.clf()

    if cur:
        curtail = pd.read_csv(mo.path.join(r_folder, "total_curtailments.csv"), index_col=0)
        plt.plot(curtail.columns, curtail.sum(axis=0) / 1e6)
        plt.xlabel("CO2_emission limit")
        plt.ylabel("Energy in GWh/year")
        plt.title("Curtailment_total")
        plt.savefig(mo.path.join(r_folder, "curtailment.png"), dpi=600)
        plt.clf()


def output_folder_list(data_folder_name):
    if mo.path.isdir(mo.path.join(mo.output_path, data_folder_name)):
        folder_list = mo.listdir(mo.path.join(mo.output_path, data_folder_name))
        folder_list.remove("results")
        print("stored a list")
        return folder_list, mo.path.join(mo.output_path, data_folder_name)
    else:
        print("output folder not found inside @" + data_folder_name)
        return list()


def stores_file(file_name, name_of_col, data_folder_name):
    folders, path = output_folder_list(data_folder_name)
    if folders != list():
        for folder in folders:
            energy_file = pd.read_csv(mo.path.join(path, folder, "results", file_name), index_col="name", parse_dates=True)
            plt.stackplot(energy_file.index, energy_file.loc[:, name_of_col], labels=[name_of_col])
            if not mo.path.isdir(mo.path.join(path, "results", name_of_col)):
                mo.mkdir(mo.path.join(path, "results", name_of_col))
            plt.savefig(mo.path.join(path, "results", name_of_col, folder + "_" + name_of_col +".png"))
            plt.legend()
            plt.title(name_of_col)
            plt.clf()
        print("saved files in " + name_of_col)


def curtailment(data_folder_name):
    folder_path = mo.path.join(mo.output_path, data_folder_name)
    folders = [str(f) for f in range(0, 185, 5)]
    folders.reverse()
    gen_p_max_pu = pd.read_csv(mo.path.join(folder_path, folders[0], "generators-p_max_pu.csv"), index_col="name", parse_dates=True)

    total_curtailments = pd.DataFrame(index=gen_p_max_pu.columns)

    for folder in folders:
        cur = pd.DataFrame(index=gen_p_max_pu.index)

        # read from folder
        gens = pd.read_csv(mo.path.join(folder_path, folder, "generators.csv"), index_col="name", parse_dates=True)
        electricity = pd.read_csv(mo.path.join(folder_path, folder, "results",  "electricity.csv"), index_col="name", parse_dates=True)

        for i in gen_p_max_pu.columns:
            cur = mo.hor(cur, ((gen_p_max_pu.loc[:, i] * gens.loc[i, "p_nom_opt"]) - electricity.loc[:, i]))

        # save individual curtailment
        cur.to_csv(mo.path.join(folder_path, folder, "results", "curtailments.csv"))

        # dataframe of total curtailments
        total_curtailments[folder] = cur.sum(axis=0)

        # save total curtailments
        total_curtailments.to_csv(mo.path.join(mo.output_path, data_folder_name, "results", "total_curtailments.csv"))


if __name__ == "__main__":
    curtailment("fi_3.0.1")
    vis_new("fi_3.0.1", cur=True)



