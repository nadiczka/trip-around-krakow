from typing import List
from datetime import datetime, timedelta
from databasepackage.data_base import DataBase
import random
import numpy as np
from copy import deepcopy

START_TIME = datetime.now()


class InnerParticle:
    def __init__(self, index_array: List[int]):
        self.current_position = index_array
        random.shuffle(self.current_position)
        self.personal_best = self.current_position
        self.v = np.floor(np.random.rand(1, 1) * len(index_array))


def switch_positions(_input: List, first_pos: int, sec_pos: int) -> List:
    result = []
    first_pos = first_pos % len(_input)
    sec_pos = sec_pos % len(_input)
    if first_pos == sec_pos:
        return _input
    elif first_pos < sec_pos:
        for i in range(first_pos):
            result.append(_input[i])
        result.append(_input[sec_pos])
        for i in range(first_pos + 1, sec_pos):
            result.append(_input[i])
        result.append(_input[first_pos])
        for i in range(sec_pos + 1, len(_input)):
            result.append(_input[i])
        return result
    else:
        for i in range(sec_pos):
            result.append(_input[i])
        result.append(_input[first_pos])
        for i in range(sec_pos + 1, first_pos):
            result.append(_input[i])
        result.append(_input[sec_pos])
        for i in range(first_pos + 1, len(_input)):
            result.append(_input[i])
        return result


def find_index(_input: List[int], am: int) -> int:
    for i in range(len(_input)):
        if _input[i] == am:
            return i
    raise IndexError


def is_correct(
        selected_monuments: List[int],
        databaseinstance: DataBase,
        numb_of_particles
) -> dict:
    index_array = create_item_sequence(selected_monuments)

    particles = []
    global_best = []

    # Tworzę cząsteczki
    for i in range(numb_of_particles):
        particles.append(InnerParticle(index_array))
        if (check_cost_limit(particles[i].current_position, databaseinstance)
                and check_time_limits(particles[i].current_position, databaseinstance)):
            return {"monums": particles[i].current_position, "time": (datetime.now() - START_TIME).total_seconds()}
        if not global_best:
            global_best = particles[i].current_position
        if get_cost(particles[i].current_position, databaseinstance) < get_cost(global_best, databaseinstance):
            global_best = particles[i].current_position

    for i in range(len(index_array)):
        for particle in particles:
            temp_g_v = int(np.floor(0.999 * np.random.rand(1, 1) * len(index_array))[0][0])
            temp_p_v = int(np.floor(0.999 * np.random.rand(1, 1) * len(index_array))[0][0])
            particle.current_position = switch_positions(particle.current_position, temp_p_v,
                                                         find_index(particle.current_position,
                                                                    particle.personal_best[temp_p_v]))
            particle.current_position = switch_positions(particle.current_position, temp_g_v,
                                                         find_index(particle.current_position,
                                                                    global_best[temp_g_v]))
            particle.v = int(np.floor((temp_p_v + temp_g_v + particle.v) / 3))
            particle.current_position = switch_positions(particle.current_position, particle.v, particle.v + 1)
            if check_cost_limit(particle.current_position, databaseinstance) and check_time_limits(
                    particle.current_position, databaseinstance):
                return {"monums": particle.current_position, "time": (datetime.now() - START_TIME).total_seconds()}
            if get_cost(particle.current_position, databaseinstance) < get_cost(particle.personal_best,
                                                                                databaseinstance):
                particle.personal_best = deepcopy(particle.current_position)
            if get_cost(particle.current_position, databaseinstance) < get_cost(global_best, databaseinstance):
                global_best = deepcopy(particle.current_position)

    raise IndexError


def get_cost(selected_monuments: List[int], databaseinstance: DataBase) -> int:
    if len(selected_monuments) == 0:
        return 0
    if len(selected_monuments) == 1:
        return databaseinstance.get_monument_by_id(selected_monuments[0]).get("cost")
    result = databaseinstance.get_monument_by_id(selected_monuments[0]).get("cost")
    for i in range(1, len(selected_monuments)):
        result = result + databaseinstance.get_cost(selected_monuments[i],
                                                    selected_monuments[i - 1]) + databaseinstance.get_monument_by_id(
            selected_monuments[i]).get("cost")
    return result


def create_item_sequence(
        monuments: List[int]
) -> List[int]:
    indexes = []
    for i in range(len(monuments)):
        if monuments[i] == 1:
            indexes.append(i)
    return indexes


def check_cost_limit(
        ordered_array: List[int],
        databaseinstance: DataBase
) -> bool:
    return get_cost(ordered_array, databaseinstance) <= databaseinstance.max_cost


def check_time_limits(
        ordered_array: List[int],
        databaseinstance: DataBase
) -> bool:
    monuments = databaseinstance.monuments
    start = databaseinstance.start_time.split('.')
    end = databaseinstance.end_time.split('.')
    # convert start and end time of tour to datetime
    start_date_str = '2020-01-01 ' + start[0] + ':' + start[1]
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M')

    end_date_str = '2020-01-01 ' + end[0] + ':' + end[1]
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')

    time_max = ((end_date - start_date).total_seconds()) // 60

    mon_amount = len(ordered_array)

    for i in range(mon_amount):

        idx = ordered_array[i]
        mon = monuments[idx]

        if not mon["open"].get("unlimited"):
            # convert start and end time of opening monument to datetime
            start_open_str = '2020-01-01 ' + mon["open"]["from"] + ':00'
            start_open = datetime.strptime(start_open_str, '%Y-%m-%d %H:%M')

            end_open_str = '2020-01-01 ' + mon["open"]["to"] + ':00'
            end_open = datetime.strptime(end_open_str, '%Y-%m-%d %H:%M')

            # check if time we want to start visiting is in range of opening hours
            if start_date < start_open or start_date > end_open:
                return False

        # get end hour of visiting monument
        start_date += timedelta(minutes=mon["time"])

        # check if time we want to end visiting is not after the monument is closed
        if not mon["open"].get("unlimited"):
            if start_date > end_open:
                return False

        # check if time of tour is not exceeded
        if end_date < start_date:
            return False

        # check if this is not last monument
        if i != (mon_amount - 1):
            next_idx = ordered_array[i + 1]

            # get end hour of moving to next monument
            start_date += timedelta(minutes=databaseinstance.get_time(idx, next_idx))

    time_lasts = ((end_date - start_date).total_seconds()) // 60
    time_consumption_factor = 1 - (time_lasts / time_max)

    return time_consumption_factor
