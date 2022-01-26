import pandas as pd
import mopy as mo
import matplotlib.pyplot as plt
import numpy as np


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


def vis_new(data_folder_name):
    r_folder = mo.path.join(mo.output_path, data_folder_name, "results")

    # electricity = pd.read_csv(mo.path.join(r_folder, "electricity_total.csv"), index_col=0)
    # heat = pd.read_csv(mo.path.join(r_folder, "heat_total.csv"), index_col=0)
    # hydrogen = pd.read_csv(mo.path.join(r_folder, "hydrogen_total.csv"), index_col=0)
    # opt = pd.read_csv(mo.path.join(r_folder, "opt.csv"), index_col=0)
    cost = pd.read_csv(mo.path.join(r_folder, "cost.csv"), index_col=0)

    # if not mo.path.isdir(mo.path.join(r_folder, "electricity_total_ind")):
    #     mo.mkdir(mo.path.join(r_folder, "electricity_total_ind"))
    # vis_ind(abs(electricity), "electricity_total", mo.path.join(r_folder, "electricity_total_ind"))
    #
    # if not mo.path.isdir(mo.path.join(r_folder, "hydrogen_total_ind")):
    #     mo.mkdir(mo.path.join(r_folder, "hydrogen_total_ind"))
    # vis_ind(abs(hydrogen), "hydrogen_total", mo.path.join(r_folder, "hydrogen_total_ind"))
    #
    # if not mo.path.isdir(mo.path.join(r_folder, "heat_total_ind")):
    #     mo.mkdir(mo.path.join(r_folder, "heat_total_ind"))
    # vis_ind(abs(heat), "heat_total", mo.path.join(r_folder, "heat_total_ind"))
    #
    # if not mo.path.isdir(mo.path.join(r_folder, "opt_ind")):
    #     mo.mkdir(mo.path.join(r_folder, "opt_ind"))
    # vis_ind(opt, "opt", mo.path.join(r_folder, "opt_ind"))


    # cost plot
    plt.plot(cost.columns, cost.sum(axis=0)/1e9)
    plt.xlabel("CO2_emission limit")
    plt.ylabel("Total costs in billion Euro")
    plt.title("Cost of reducing the CO2 emissions")
    plt.savefig(mo.path.join(r_folder, "cost.png"), dpi=600)
    plt.clf()
    # plt.show

    # area plot
    # print(heat)
    # plt.stackplot(heat.columns,  heat.iloc[[0, 1, 3], :], labels=["a", "b", "c"])
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    vis_new("fi_3.0.1")






