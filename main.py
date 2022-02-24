import csv

from algorithm.target_function import target_fun, calc_types
from databasepackage.data_base import DataBase, config_read
from graphics.gui import start_fun, AlgorithmProgressWindow
from algorithm.main_PSO_algorithm import main_PSO_algorithm
from algorithm.is_correct import check_time_limits, get_cost
from algorithm.final_min_prior import create_final_min_priority


from config_reader import *
write_logs = False
new_init_points = None
if read_init_points:
    new_init_points = []
    for i in range(number_of_particles):
        with open('logs/log' + str(i) + ".csv", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                new_init_points.append([int(float(el)) for el in row])
                break

dataBaseInstance = DataBase(file_path=file_path,
                            start_time=start_time,
                            end_time=end_time,
                            velocity=velocity,
                            travel_cost=travel_cost,
                            max_cost=max_cost,
                            randomising_cost=randomising_cost,
                            randomising_time=randomising_time)

min_prior = create_final_min_priority(min_prior, dataBaseInstance, factors, configs["proportionality_factor"])

if display_progress:
    window = AlgorithmProgressWindow(dataBaseInstance, number_of_particles=number_of_particles, ratios=ratios,
                                     min_priority=min_prior, boredom_ratio=boredom_ratio, map_path=map_path,
                                     numb_of_particles_inner=number_of_particles_inner)
else:
    result = main_PSO_algorithm(dataBaseInstance, ratios, boredom_ratio, init_points=new_init_points,
                                min_priority=min_prior, number_of_particles=number_of_particles,
                                numb_of_particles_inner=number_of_particles_inner)
    global_best = result.get("global_best")
    globs = result.get("globs")

    print("\n\nRozwiązanie ostateczne to:")
    print(global_best)
    print(target_fun(global_best, dataBaseInstance, ratios, boredom_ratio))
    print("Kolejnosc zwiedzania zabytkow:", globs[-1].get("monums"))
    print("Typy zabytków:")
    print(calc_types(global_best, dataBaseInstance))
    print("Procent wykorzystanego czasu: ",
          "{:.2f}".format(check_time_limits(globs[-1].get("monums"), dataBaseInstance)))
    print("Procent wykorzystanego kosztu: ",
          "{:.2f}".format((get_cost(globs[-1].get("monums"), dataBaseInstance)) / dataBaseInstance.max_cost))
    start_fun(globs, dataBaseInstance, map_path)

if write_logs:
    logs = result["logs"]
    for i in logs.keys():
        with open('logs/log' + str(i) + '.csv', 'w', newline='') as f:
            f.truncate()
            for k in range(len(logs[i])):
                writer = csv.writer(f)
                writer.writerow(logs[i][k])
