from algorithm.sensitivity_factors import calculate_sensitivity_cost, \
    calculate_sensitivity_time, calculate_sensitivity_size
from algorithm.target_function import count_min_priority
from graphics.plot_fun import save_new_plot


def create_final_min_priority(min_prior, dataBaseInstance, factors, prop_factor):
    if min_prior > 0:
        min_prior = min_prior
    else:
        min_prior = count_min_priority(dataBaseInstance, factors=factors)
        xs, ys = calculate_sensitivity_cost(dataBaseInstance, 1, 1, (0.5, 1.5), 0.001,
                                            float(prop_factor))
        save_new_plot(xs, ys, "cost_sensitivity", "cost_factor", "sensitivity", (4, 4),
                                "Czułość cost_factor",
                                "bo")
        xs, ys = calculate_sensitivity_size(dataBaseInstance, 1, 1, (0.5, 1.5), 0.001,
                                            float(prop_factor))
        save_new_plot(xs, ys, "size_sensitivity", "size_factor", "sensitivity", (4, 4),
                                "Czułość size_factor",
                                "bo")
        xs, ys = calculate_sensitivity_time(dataBaseInstance, 1, 1, (0.5, 1.5), 0.001,
                                            float(prop_factor))
        save_new_plot(xs, ys, "time_sensitivity", "time_factor", "sensitivity", (4, 4),
                                "Czułość time_factor",
                                "bo")
    return min_prior
