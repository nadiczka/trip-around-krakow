import numpy as np
from databasepackage.data_base import DataBase
from algorithm.target_function import count_min_priority


def calculate_sensitivity_cost(databaseinstance: DataBase, time_factor: float, size_factor: float, limits: tuple,
                               dp: float, proportionality_factor: float):
    p_0 = limits[0]
    u_0 = count_min_priority(databaseinstance,
                             {"cost_factor": p_0, "size_factor": size_factor, "time_factor": time_factor,
                              "proportionality_factor": proportionality_factor})
    ps = [p_0 + dp * n for n in range(1, int(np.floor((limits[1] - limits[0]) / dp)))]
    us = []
    ss = []
    for index in range(len(ps)):
        us.append(count_min_priority(databaseinstance,
                                    {"cost_factor": ps[index], "size_factor": size_factor, "time_factor": time_factor,
                                     "proportionality_factor": proportionality_factor}))
        if index != 0:
            s_temp = (ps[index] / us[index]) * ((us[index] - us[index - 1]) / dp)
        else:
            s_temp = (ps[index] / us[index]) * ((us[index] - u_0) / dp)
        ss.append(s_temp)
    return ps, ss


def calculate_sensitivity_time(databaseinstance: DataBase, cost_factor: float, size_factor: float, limits: tuple,
                               dp: float, proportionality_factor: float):
    p_0 = limits[0]
    u_0 = count_min_priority(databaseinstance,
                             {"time_factor": p_0, "size_factor": size_factor, "cost_factor": cost_factor,
                              "proportionality_factor": proportionality_factor})
    ps = [p_0 + dp * n for n in range(1, int(np.floor((limits[1] - limits[0]) / dp)))]
    ss = []
    us = []
    for index in range(len(ps)):
        us.append(count_min_priority(databaseinstance,
                                    {"time_factor": ps[index], "size_factor": size_factor, "cost_factor": cost_factor,
                                     "proportionality_factor": proportionality_factor}))
        if index != 0:
            s_temp = (ps[index] / us[index]) * ((us[index] - us[index - 1]) / dp)
        else:
            s_temp = (ps[index] / us[index]) * ((us[index] - u_0) / dp)
        ss.append(s_temp)
    return ps, ss


def calculate_sensitivity_size(databaseinstance: DataBase, cost_factor: float, time_factor: float, limits: tuple,
                               dp: float, proportionality_factor: float):
    p_0 = limits[0]
    u_0 = count_min_priority(databaseinstance,
                             {"size_factor": p_0, "time_factor": time_factor, "cost_factor": cost_factor,
                              "proportionality_factor": proportionality_factor})
    ps = [p_0 + dp * n for n in range(1, int(np.floor((limits[1] - limits[0]) / dp)))]
    ss = []
    us = []
    for index in range(len(ps)):
        us.append(count_min_priority(databaseinstance,
                                    {"size_factor": ps[index], "time_factor": time_factor, "cost_factor": cost_factor,
                                     "proportionality_factor": proportionality_factor}))
        if index != 0:
            s_temp = (ps[index] / us[index]) * ((us[index] - us[index - 1]) / dp)
        else:
            s_temp = (ps[index] / us[index]) * ((us[index] - u_0) / dp)
        ss.append(s_temp)
    return ps, ss
