import matplotlib.pyplot as plt
from databasepackage.data_base import DataBase
from graphics.gui import convert_to_x_and_y


def save_plot_fun(databaseinstance: DataBase, chosen: list, name: str, size: tuple):
    xs, ys = convert_to_x_and_y(chosen, databaseinstance)
    plt.figure(figsize=size)
    plt.plot(xs, ys, "-bo")
    img = plt.imread("files/mapa.png")
    plt.imshow(img)
    plt.savefig("../pictures/" + name + ".png")
    plt.close()


def save_new_plot(xs: list, ys: list, name: str, xlabel: str, ylabel: str, size: tuple, title: str,
                            style: str):
    plt.figure(figsize=size)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(xs, ys, style)
    try:
        plt.savefig("../pictures/" + name + ".png")
    except FileNotFoundError:
        plt.savefig("pictures/" + name + ".png")
    plt.close()


def save_plot_from_xy(x, y, name: str, title: str, subtitle: str, type: str):
    if type == "iter":
        xlabel = "algorithm iteration"
    elif type == "time":
        xlabel = "time from start in seconds"

    size = (30, 15)
    plt.figure(figsize=size)
    plt.xlabel(xlabel, fontsize=35)
    plt.ylabel("value of target function", fontsize=35)
    plt.suptitle(title, fontsize=50)
    plt.title(subtitle, fontsize=35)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if x[len(x) - 1] + 0.05 * x[len(x) - 1] != 0:
        plt.xlim([0, x[len(x) - 1] + 0.05 * x[len(x) - 1]])
    plt.ylim([0, y[len(y) - 1] + 0.05 * y[len(y) - 1]])
    plt.plot(x, y, "bo", markersize=25)
    plt.savefig("../pictures/" + name + "_" + type + ".png")
    plt.close()

    print("Utworzono wykres " + type)
