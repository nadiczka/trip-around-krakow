from algorithm.target_function import target_fun, count_min_priority
from algorithm.is_correct import is_correct
from copy import deepcopy
import numpy as np
from databasepackage.data_base import DataBase


class Particle:
    def __init__(self, length: int, id: int, init_points: list, logging_generate: bool, dataBaseInstance: DataBase,
                 chance_zero: float, numb_of_particles_inner):
        self.id = id
        if not init_points:
            self.X_i = np.round(np.random.rand(1, length))[0].tolist()
            while True:
                if logging_generate:
                    print("generating...")
                try:
                    is_correct(self.X_i, dataBaseInstance, numb_of_particles=numb_of_particles_inner)
                    break
                except IndexError:
                    self.X_i = np.round(np.random.rand(1, length) * 0.5 / chance_zero)[0].tolist()
        else:
            self.X_i = init_points[self.id]
        self.v = np.floor(np.random.rand(1, 1) * length)
        self.personal_best = self.X_i


def main_PSO_algorithm(
        dataBaseInstance,
        ratios,
        boredom_ratio,
        number_of_particles,
        numb_of_particles_inner,
        min_priority=None,
        display_window=None,
        logging_generate=True,
        chance_zero=0.7,
        init_points=None,
        logging=True,
):
    min_accept_priority = min_priority

    globs = []
    global_best = []
    particles = []
    logs = {}

    for c in range(number_of_particles):
        particles.append(Particle(
            dataBaseInstance.number_of_monuments, c, init_points, logging_generate, dataBaseInstance, chance_zero,
            numb_of_particles_inner
        ))
        if logging:
            logs[particles[c].id] = []
            logs[particles[c].id].append(particles[c].X_i)
        if target_fun(particles[c].X_i, dataBaseInstance, ratios, boredom_ratio) > target_fun(global_best,
                                                                                              dataBaseInstance, ratios,
                                                                                              boredom_ratio):
            global_best = particles[c].X_i

    print("\nWartosc minimalnego priorytetu:", min_accept_priority, "\n")

    glob_changes = []
    priorities = []
    glob_changes.append(0)
    iter_counter = 0
    while True:
        try:
            temp_dict = is_correct(global_best, dataBaseInstance, numb_of_particles_inner)
            temp_dict["priority"] = target_fun(global_best, dataBaseInstance, ratios, boredom_ratio)
            globs.append(temp_dict)
            priorities.append(temp_dict["priority"])
            if display_window:
                display_window.display_position(temp_dict["monums"], temp_dict["priority"])
            break
        except IndexError:
            pass

    while target_fun(deepcopy(global_best), dataBaseInstance, ratios, boredom_ratio) < min_accept_priority:
        iter_counter = iter_counter + 1
        for c in particles:
            while True:
                p = int(np.floor(np.random.rand(1, 1) * len(c.X_i))[0][0])
                g = int(np.floor(np.random.rand(1, 1) * len(c.X_i))[0][0])
                v = int(np.floor((p + g + c.v) / 3))
                temp_X_i = deepcopy(c.X_i)
                temp_X_i[p] = c.personal_best[p]
                temp_X_i[g] = global_best[g]
                temp_X_i[v] = (c.X_i[v] + 1) % 2
                try:
                    order_list = is_correct(temp_X_i, dataBaseInstance, numb_of_particles_inner)
                    c.v = v
                    c.X_i = temp_X_i
                    if logging:
                        logs[c.id].append(c.X_i)
                    break
                except IndexError:
                    pass

            if target_fun(c.X_i, dataBaseInstance, ratios, boredom_ratio) > target_fun(c.personal_best,
                                                                                       dataBaseInstance, ratios,
                                                                                       boredom_ratio):
                c.personal_best = deepcopy(c.X_i)
            if target_fun(c.X_i, dataBaseInstance, ratios, boredom_ratio) > target_fun(deepcopy(global_best),
                                                                                       dataBaseInstance, ratios,
                                                                                       boredom_ratio):
                print(global_best)
                print(target_fun(deepcopy(global_best), dataBaseInstance, ratios, boredom_ratio))
                global_best = deepcopy(c.X_i)
                order_list["priority"] = target_fun(deepcopy(global_best), dataBaseInstance, ratios, boredom_ratio)
                priorities.append(order_list["priority"])
                if display_window:
                    display_window.display_position(global_best, order_list["priority"])
                globs.append(deepcopy(order_list))
                glob_changes.append(iter_counter)

    result = {"global_best": global_best, "globs": globs, "glob_changes": glob_changes}
    if logging:
        result["logs"] = logs
    return result
