
from databasepackage.data_base import config_read

try:
    configs = config_read("../files/config.csv")
except FileNotFoundError:
    configs = config_read("files/config.csv")

display_progress = configs["gui"] == "True"  # done
write_logs = configs["write_logs"] == "True"  # done
read_init_points = configs["read_init_points"] == "True"  # done
min_prior = float(configs["min_prior"])  # done
start_time = str(configs["start_time"])  # done
end_time = str(configs["end_time"])  # done
velocity = float(configs["velocity"])  # done
travel_cost = float(configs["travel_cost"])  # done
max_cost = float(configs["max_cost"])  # done
randomising_time = float(configs["randomising_time"])  # done
randomising_cost = float(configs["randomising_cost"])  # done
number_of_particles_inner = int(configs["numb_of_particles_inner"])  # done
number_of_particles = int(configs["numb_of_particles"])  # done
file_path = str(configs["file_path"])  # done
map_path = str(configs["map_path"])  # done
boredom_ratio = float(configs["boredom_ratio"])  # done
factors = {
    "cost_factor": float(configs["cost_factor"]),
    "time_factor": float(configs["time_factor"]),
    "size_factor": float(configs["size_factor"]),
    "proportionality_factor": float(configs["proportionality_factor"])
}  # done

ratios = {
    "castle": float(configs["castle_ratio"]),
    "church": float(configs["church_ratio"]),
    "memorial": float(configs["memorial_ratio"]),
    "culture": float(configs["culture_ratio"]),
    "pub": float(configs["pub_ratio"]),
    "other": float(configs["other_ratio"]),
}  # done
