import csv
from algorithm.main_PSO_algorithm import main_PSO_algorithm
from graphics.plot_fun import save_plot_from_xy
from config_reader import *
from algorithm.target_function import calc_types
from algorithm.is_correct import check_time_limits, get_cost
from algorithm.final_min_prior import create_final_min_priority
from graphics.gui import start_fun


def convert_result_to_data_time_for_plot(result):
    globs = result.get("globs")
    x = []
    y = []
    for el in globs:
        x.append(el.get("time"))
        y.append(el.get("priority"))
    return x, y

new_init_points = None
if read_init_points:
    new_init_points = []
    for i in range(number_of_particles):
        with open('../logs/log' + str(i) + ".csv", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                new_init_points.append([int(float(el)) for el in row])
                break


def create_plot_data(databaseinstance, result, name, title):
    # do wykresow
    (xtime, y) = convert_result_to_data_time_for_plot(result)
    xiter = result["glob_changes"]
    monums = result["globs"][len(result["globs"]) - 1]["monums"]
    subtitle = databaseinstance.get_monument_by_id(monums[0]).get("name")
    for index in range(1, len(monums) - 1):
        subtitle = subtitle + "->" + databaseinstance.get_monument_by_id(monums[index]).get("name")
    save_plot_from_xy(xiter, y, name, title, subtitle, 'iter')
    save_plot_from_xy(xtime, y, name, title, subtitle, 'time')


def base_test_form_data(databaseinstance, name, title, costumed_boredom_ratio=None, number_of_it=10, block_plot=None, block_gui=None):
    time_cons_factor = 0
    cost_cons_factor = 0
    categories = {"castle": 0, "church": 0, "memorial": 0, "culture": 0, "pub": 0, "other": 0}
    for i in range(number_of_it):
        min_priority = create_final_min_priority(min_prior, databaseinstance, factors, configs["proportionality_factor"])

        if not costumed_boredom_ratio:
            costumed_boredom_ratio = boredom_ratio

        result = main_PSO_algorithm(databaseinstance,
                                    min_priority=min_priority,
                                    ratios=ratios,
                                    boredom_ratio=costumed_boredom_ratio,
                                    init_points=new_init_points,
                                    number_of_particles=number_of_particles,
                                    numb_of_particles_inner=number_of_particles_inner)

        if write_logs:
            logs = result["logs"]
            for i in logs.keys():
                with open('../logs/log' + str(i) + '.csv', 'w', newline='') as f:
                    f.truncate()
                    for k in range(len(logs[i])):
                        writer = csv.writer(f)
                        writer.writerow(logs[i][k])

        # wskazniki
        global_best = result.get("global_best")
        globs = result.get("globs")

        types = calc_types(global_best, databaseinstance)
        for key, val in types.items():
            categories[key] += val
        time_cons_factor = time_cons_factor + check_time_limits(globs[-1].get("monums"), databaseinstance)
        cost_cons_factor = cost_cons_factor + get_cost(globs[-1].get("monums"), databaseinstance)/databaseinstance.max_cost

        if i == 0:
            if not block_plot:
                create_plot_data(databaseinstance, result, name, title)
            if not block_gui:
                start_fun(globs, databaseinstance, map_path)

    for key, val in categories.items():
        categories[key] = categories[key]/number_of_it
    time_cons_factor = time_cons_factor/number_of_it
    cost_cons_factor = cost_cons_factor/number_of_it
    print("Typy zabytków:", categories)
    print("Procent wykorzystanego czasu: ", "{:.2f}".format(time_cons_factor))
    print("Procent wykorzystanego kosztu: ", "{:.2f}".format(cost_cons_factor))

    return {"time_cons_factor": time_cons_factor, "cost_cons_factor": cost_cons_factor, "categories": categories}
