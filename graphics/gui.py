import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithm.target_function import count_min_priority
from databasepackage.data_base import DataBase
import matplotlib.pyplot as plt
from algorithm.main_PSO_algorithm import main_PSO_algorithm


class PlotObjectFuck:
    def __init__(self, window: tk.Tk, map_path):
        self.map_path = map_path
        fig_width = int(window.winfo_screenmmwidth() * 0.0393701)
        fig_height = int(window.winfo_screenmmheight() * 0.0393701)
        f = plt.figure(figsize=(fig_width - 2, fig_height - 2))
        try:
            img = plt.imread(self.map_path)
        except FileNotFoundError:
            img = plt.imread("../" + self.map_path)

        plt.imshow(img)

        self.plot_cv = FigureCanvasTkAgg(f, master=window)
        plt.close()

    def pack_plot(self):
        self.plot_cv.get_tk_widget().pack()

    def replace_plot(self, f, window):
        self.plot_cv.get_tk_widget().pack_forget()
        self.plot_cv = FigureCanvasTkAgg(f, master=window)
        self.plot_cv.get_tk_widget().pack()


def convert_to_x_and_y(chosen: list, dataBaseInstance: DataBase) -> tuple:
    xs = []
    ys = []
    for index in chosen:
        xs.append(dataBaseInstance.get_monument_by_id(index).get("position")[0])
        ys.append(dataBaseInstance.get_monument_by_id(index).get("position")[1])
    return xs, ys


def start_fun(result: list, dataBaseInstance: DataBase, map_path):
    priorities = [el.get("priority") for el in result]
    result = [el.get("monums") for el in result]

    window = tk.Tk()
    window.title("Prezentacja wyników")
    first_line = tk.Label(text="Wybierz iterację:", master=window)
    first_line.pack()

    plotobjectfuck = PlotObjectFuck(window, map_path)
    chosen_iter = tk.StringVar(window)
    chosen_iter.set("0")
    choose_list = tk.OptionMenu(window, chosen_iter, *range(len(result)))
    choose_list.pack()
    active_priority = tk.StringVar(window)
    priority_label = tk.Label(window, textvariable=active_priority)
    active_priority.set("Priorytet: 0")
    priority_label.pack()
    names_var = tk.StringVar(window)
    names_var.set("Wybierz iterację")
    names_label = tk.Label(window, textvariable=names_var)
    names_label.pack()

    button_show = tk.Button(master=window, command=(
        lambda: change_string(plotobjectfuck, result, dataBaseInstance, chosen_iter, window, priorities,
                              active_priority, names_var, map_path)))
    button_show['text'] = 'Pokaż'
    button_show.pack()

    plotobjectfuck.pack_plot()

    window.mainloop()


class AlgorithmProgressWindow:
    def __init__(self, dataBaseInstance: DataBase, min_priority, ratios, number_of_particles, boredom_ratio, map_path,
                 numb_of_particles_inner):
        self.dataBaseInstance = dataBaseInstance
        self.min_priority = min_priority
        self.window = tk.Tk()
        self.window.title("Postępy algorytmu")
        self.ratios = ratios
        self.number_of_particles = number_of_particles
        self.boredom_ratio = boredom_ratio
        self.map_path = map_path
        self.numb_of_particles_inner = numb_of_particles_inner
        first_line = tk.Label(text="Obecna pozycja algorytmu:", master=self.window)
        first_line.pack()
        button_start = tk.Button(master=self.window, command=(
            lambda: self.do_algorithm()))
        button_start['text'] = 'Rozpocznij'
        button_start.pack()
        self.window.mainloop()

    def display_position(self, position: list, priority: float):
        temp_string = str(position) + " o priorytecie: " + str(priority)
        line = tk.Label(text=temp_string, master=self.window)
        line.pack()

    def do_algorithm(self):
        line = tk.Label(text=("Minimalny priorytet to:" + str(self.min_priority)), master=self.window)
        line.pack()
        result = main_PSO_algorithm(self.dataBaseInstance, min_priority=self.min_priority, display_window=self,
                                    ratios=self.ratios, number_of_particles=self.number_of_particles,
                                    boredom_ratio=self.boredom_ratio,
                                    numb_of_particles_inner=self.numb_of_particles_inner)
        start_fun(result.get("globs"), self.dataBaseInstance, map_path=self.map_path)


def change_string(to_change, all_chosen: list, dataBaseInstance: DataBase, current_line: tk.StringVar, window: tk.Tk,
                  priorities: list, active_priority: tk.StringVar, names_var: tk.StringVar, map_path):
    line = int(current_line.get())
    active_priority.set("Priorytet: " + str(priorities[line]))
    xs, ys = convert_to_x_and_y(all_chosen[line], dataBaseInstance)
    temp_string = dataBaseInstance.get_monument_by_id(all_chosen[line][0]).get("name")
    for index in range(1, len(all_chosen[line])):
        temp_string = temp_string + "->" + dataBaseInstance.get_monument_by_id(all_chosen[line][index]).get("name")
    names_var.set(temp_string)
    fig_width = int(window.winfo_screenmmwidth() * 0.0393701)
    fig_height = int(window.winfo_screenmmheight() * 0.0393701)
    f = plt.figure(figsize=(fig_width - 2, fig_height - 2))
    plt.plot(xs, ys, "-bo")
    try:
        img = plt.imread(map_path)
    except FileNotFoundError:
        img = plt.imread("../"+map_path)
    plt.imshow(img)
    try:
        plt.savefig("pictures/" + str(line) + ".png")
    except FileNotFoundError:
        plt.savefig("../pictures/" + str(line) + ".png")
    to_change.replace_plot(f, window)
    plt.close()


if __name__ == '__main__':
    dataBaseInstance = DataBase()
    temp_result_log = [
        [5, 1, 3, 2, 7],
        [9, 4, 2, 9, 1],
        [2, 1, 3, 7, 4]
    ]

    start_fun(temp_result_log, dataBaseInstance)
