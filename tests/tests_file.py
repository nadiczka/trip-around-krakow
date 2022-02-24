import matplotlib.pyplot as plt
from databasepackage.data_base import DataBase
import random
from config_reader import *
from graphics.plot_fun import save_plot_from_xy

from tests.tests_utils import base_test_form_data


def dane_bazowe_test():
    # test danych bazowych
    databaseinstance = DataBase(file_path='../files/base_basic.csv',
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                max_cost=max_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    base_test_form_data(databaseinstance,
                        name="test_dane_bazowe",
                        title="Glowna baza danych")


def zabytki_z_jednej_kategorii_test():
    # zabytki jedynie z jednej kategorii
    databaseinstance = DataBase(file_path='../files/base_churches.csv',
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                max_cost=max_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    base_test_form_data(databaseinstance,
                        name="test_zabytki_z_jednej_kategorii",
                        title="Wszystkie zabytki z jednej kategorii")


def losowe_godziny_zwiedzania_test():
    # losowe godziny zwiedzania tak aby start zwiedzania < end zwiedzania
    for i in range(10):
        hour_start_int = random.randint(8, 20)
        hour_start = str(hour_start_int) + '.00'
        hour_end_int = 0
        while hour_end_int <= hour_start_int:
            hour_end_int = random.randint(8, 20)
        hour_end = str(hour_end_int) + '.00'
        databaseinstance = DataBase(file_path='../files/base_basic.csv',
                                    start_time=hour_start,
                                    end_time=hour_end,
                                    velocity=velocity,
                                    travel_cost=travel_cost,
                                    max_cost=max_cost,
                                    randomising_cost=randomising_cost,
                                    randomising_time=randomising_time)
        base_test_form_data(databaseinstance,
                            number_of_it=2,
                            name=("test_losowe_godziny_zwiedzania"+str(hour_start)+"to"+str(hour_end)),
                            title=("Losowe  godziny zwiedzania od "+str(hour_start)+" do "+str(hour_end)))


def malo_zabytkow_test():
    # test programu przy malej ilosci zabytkow w bazie
    databaseinstance = DataBase(file_path='../files/base_minimal.csv',
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                max_cost=max_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    base_test_form_data(databaseinstance,
                        name="test_mala_ilosc_zabytkow_w_bazie",
                        title="Mala ilosc zabytkow w bazie")


def losowe_maksymalne_koszty_test():
    # losowe godziny zwiedzania tak aby start zwiedzania < end zwiedzania
    for i in range(10):
        max_cost = random.randint(0, 1000)
        databaseinstance = DataBase(file_path='../files/base_basic.csv',
                                    max_cost=max_cost,
                                    start_time=start_time,
                                    end_time=end_time,
                                    velocity=velocity,
                                    travel_cost=travel_cost,
                                    randomising_cost=randomising_cost,
                                    randomising_time=randomising_time)
        base_test_form_data(databaseinstance,
                            name=("test_losowe_maksymalne_koszty"+str(max_cost)),
                            title="Losowy maksymalny koszt = "+str(max_cost))


def dominujacy_zabytek_test():
    # test programu gdy jeden zabytek ma duzo wiekszy priorytet (tu BARBAKAN)
    databaseinstance = DataBase(file_path='../files/base_dominated_priority.csv.csv',
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                max_cost=max_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    base_test_form_data(databaseinstance,
                        name="test_dominujacy_priorytet_barbakan",
                        title="Zabytek o dominujacym priorytecie - Barbakan")


def losowe_boredom_ratio_test():
    # losowe boredom ratio z zakresu 0.8 - 0.9
    x = []
    ytime = []
    ycost = []
    databaseinstance = DataBase(file_path='../files/base_basic.csv',
                                max_cost=max_cost,
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    for i in range(4):
        boredom_ratio = random.uniform(0.82, 0.9)
        res = base_test_form_data(databaseinstance,
                                  number_of_it=2,
                                  block_plot=True,
                                  costumed_boredom_ratio=boredom_ratio,
                                  name=("test_losowe_boredom_ratio"+str(boredom_ratio)),
                                  title="Losowy boredom ratio = "+str(boredom_ratio))
        x.append(boredom_ratio)
        ytime.append(res["time_cons_factor"])
        ycost.append(res["cost_cons_factor"])

    save_plot_from_xy(x, ytime, "test_losowe_boredom_ratio_time", "Test losowe boredom ratio wspolczynnik czasu", "", "time_fact")
    save_plot_from_xy(x, ycost, "test_losowe_boredom_ratio_cost", "Test losowe boredom ratio wspolczynnik kosztu", "", "cost_fact")


def inne_kategorie_test():
    # test dróżnych kategorii
    databaseinstance = DataBase(file_path='../files/base_basic.csv',
                                start_time=start_time,
                                end_time=end_time,
                                velocity=velocity,
                                travel_cost=travel_cost,
                                max_cost=max_cost,
                                randomising_cost=randomising_cost,
                                randomising_time=randomising_time)
    base_test_form_data(databaseinstance,
                        name="test_bore_1",
                        title="Każdy zabytek z innej kategorii",)


inne_kategorie_test()
#dane_bazowe_test()
# zabytki_z_jednej_kategorii_test()
# losowe_godziny_zwiedzania_test()
# malo_zabytkow_test()
# losowe_maksymalne_koszty_test()