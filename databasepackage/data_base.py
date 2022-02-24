import csv
import numpy as np


class DataBase:
    # konstruktor z wartościami domyślnymi
    monuments = []
    cost_matrix = {}
    time_matrix = {}

    def __init__(
            self,
            file_path,
            start_time=None,
            end_time=None,
            velocity=None,
            travel_cost=None,
            max_cost=None,
            randomising_time=0.0,
            randomising_cost=0.0):

        # tour hours
        self.start_time = start_time
        self.end_time = end_time
        self.randomising_time = randomising_time
        self.randomising_cost = randomising_cost

        self.velocity = velocity
        self.travel_cost = travel_cost

        # cost of tour
        self.max_cost = max_cost

        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.add_monument(self.monument_list_to_dict(row))

            # monuments
            #   name: name of monument
            #   time: visiting time in MINUTES
            #   cost: entrance fee
            #   open: open hours  - we can check try: mon_1["open"].get("unlimited") and if there is "unlimited" key
            #                       in "open", then it return True or False if it is not
            #   category: category of monument
            #   priority: form 1 to 10

        self.number_of_monuments = len(self.monuments)

    def get_monument_by_id(self, _id: int) -> dict:
        for monument in self.monuments:
            if monument.get("id") == _id:
                return monument
        raise IndexError

    def get_max_id(self) -> int:
        temp_res = 0
        try:
            if not self.monuments:
                raise IndexError
        except AttributeError:
            raise IndexError
        for monument in self.monuments:
            if monument.get("id") > temp_res:
                temp_res = monument.get("id")
        return temp_res

    def add_monument(self, monument_: dict):
        try:
            monument_["id"] = self.get_max_id() + 1
        except IndexError:
            monument_["id"] = 0

        for mon in self.monuments:

            self.cost_matrix[(monument_["id"], mon["id"])] = (abs(monument_["position"][0] - mon["position"][0]) + abs(
                monument_["position"][1] - mon["position"][1])) * (
                    1 - self.randomising_cost / 2 + self.randomising_cost * (np.random.rand(1, 1))[0][0]) * self.travel_cost
            self.cost_matrix[(mon["id"], monument_["id"])] = (abs(monument_["position"][0] - mon["position"][0]) + abs(
                monument_["position"][1] - mon["position"][1])) * (1 - self.randomising_cost / 2 + self.randomising_cost *
                    (np.random.rand(1, 1))[0][0]) * self.travel_cost
            self.time_matrix[(monument_["id"], mon["id"])] = (abs(monument_["position"][0] - mon["position"][0]) + abs(
                monument_["position"][1] - mon["position"][1])) * (1 - self.randomising_time / 2 + self.randomising_time *
                    (np.random.rand(1, 1))[0][0]) / self.velocity
            self.time_matrix[(mon["id"], monument_["id"])] = (abs(monument_["position"][0] - mon["position"][0]) + abs(
                monument_["position"][1] - mon["position"][1])) * (1 - self.randomising_time / 2 + self.randomising_time *
                    (np.random.rand(1, 1))[0][0]) / self.velocity
        self.monuments.append(monument_)

    def monument_list_to_dict(self, monument_: list) -> dict:
        if monument_[3] != "unlimited":
            res_dict = {"name": monument_[0], "time": int(monument_[1]), "cost": int(monument_[2]),
                        "open": {"from": monument_[3], "to": monument_[4]}, "category": monument_[5],
                        "priority": int(monument_[6]), "position": (int(monument_[7]), int(monument_[8]))}
        else:
            res_dict = {"name": monument_[0], "time": int(monument_[1]), "cost": int(monument_[2]),
                        "open": {"unlimited": True}, "category": monument_[5],
                        "priority": int(monument_[6]), "position": (int(monument_[7]), int(monument_[8]))}
        return res_dict

    def matrix_to_dict(self, matrix_):
        res_dict = {}
        for id1 in range(len(matrix_)):
            for id2 in range(len(matrix_[id1])):
                res_dict[(id1, id2)] = matrix_[id1][id2]
        return res_dict

    def get_cost(self, id1: int, id2: int) -> int:
        return self.cost_matrix[(id1, id2)]

    def get_time(self, id1: int, id2: int) -> int:
        return self.time_matrix[(id1, id2)]


def config_read(file_path):
    config = {}
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            config[row[0]] = row[1]
    return config
