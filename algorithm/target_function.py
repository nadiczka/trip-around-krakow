from typing import List
from databasepackage.data_base import DataBase
from datetime import datetime


def target_fun(
        checked_monuments: List[int],
        databaseinstance: DataBase,
        ratios,
        boredom_ratio
) -> float:
    priorities_with_boredom = 0
    switcher = {
        "castle": 0,
        "church": 0,
        "memorial": 0,
        "culture": 0,
        "pub": 0,
        "other": 0
    }
    for i in range(len(checked_monuments)):
        if checked_monuments[i] != 0:
            current_category = databaseinstance.get_monument_by_id(_id=i).get("category")
            if current_category in switcher.keys():
                switcher[current_category] += 1
            else:
                return False
    for i in range(len(checked_monuments)):
        if checked_monuments[i] != 0:
            priority_value = databaseinstance.get_monument_by_id(_id=i).get("priority")
            current_category = databaseinstance.get_monument_by_id(_id=i).get("category")
            priorities_with_boredom += ratios.get(current_category) * priority_value * (boredom_ratio ** (switcher.get(current_category) - 1))
    return priorities_with_boredom


def count_min_priority(databaseinstance: DataBase, factors) -> int:

    sum = {
        "time": 0,
        "cost": 0,
        "priority": 0,
    }
    cost_factor = factors["cost_factor"]
    time_factor = factors["time_factor"]
    size_factor = factors["size_factor"]
    proportionality_factor = factors["proportionality_factor"]

    for id in range(databaseinstance.get_max_id() + 1):
        monument = databaseinstance.get_monument_by_id(id)
        for key, value in sum.items():
            sum[key] = value + monument[key]

    start = databaseinstance.start_time.split('.')
    end = databaseinstance.end_time.split('.')
    start_date = datetime.strptime('2020-01-01 ' + start[0] + ':' + start[1], '%Y-%m-%d %H:%M')
    end_date = datetime.strptime('2020-01-01 ' + end[0] + ':' + end[1], '%Y-%m-%d %H:%M')

    visiting = {
        "time": int((end_date - start_date).seconds/60),
        "cost": databaseinstance.max_cost,
    }

    part_priority = {}
    for key, value in visiting.items():
        part_value = value / sum[key] if value / sum[key] <= 1 else 1
        part_priority[key] = part_value * sum["priority"] * size_factor

    average_min_priority = (cost_factor*part_priority["cost"]+time_factor*part_priority["time"])/2

    # proportionality_factor = 1.006**(-0.8*average_min_priority)
    # print("\n\n\n", proportionality_factor, "\n")

    end_min_priority = proportionality_factor*average_min_priority
    return end_min_priority


def calc_types(checked_monuments: List[int], databaseinstance: DataBase):
    switcher = {
        "castle": 0,
        "church": 0,
        "memorial": 0,
        "culture": 0,
        "pub": 0,
        "other": 0
    }
    for i in range(len(checked_monuments)):
        if checked_monuments[i] != 0:
            current_category = databaseinstance.get_monument_by_id(_id=i).get("category")
            if current_category in switcher.keys():
                switcher[current_category] += 1
            else:
                return False
    return switcher