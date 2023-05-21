import numpy as np
from dataclasses import dataclass
import timeit
from meta_heuristics import MetaHeuristics
from Agenda_OTM import Optimize_Operation

# Case test data

n_days = 36
n_ug = 5
n_rounds = 1

maintenance_duration = [[5, ],
                        [8, ],
                        [6, ],
                        [6, ],
                        [3, ]]

a = np.sort(maintenance_duration)
dm_sort = np.zeros(shape=(n_ug, n_rounds))
for im in range(n_rounds):
    for it in range(n_ug):
        dm_sort[it, im] = int(a[it, n_rounds - im - 1])

maintenance_duration = dm_sort

# rfo = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#
# rfo = np.array(rfo)
rfo = np.zeros(shape=(n_ug, n_days))

vaz_afl_aux = [19883.921589, 20203.761685, 20461.283812, 20601.945018, 20905.857038, 21260.502071,
               21688.485437, 21988.058147, 22271.553480, 22545.329996, 22761.029453, 22967.500212,
               23150.803255, 23340.732115, 23574.452067, 23908.813747, 24257.863790, 24635.077246,
               24951.345853, 25239.747806, 25610.109852, 25957.051659, 26155.295278, 26288.031591,
               26448.608253, 26584.237494, 26772.100663, 26951.747644, 27088.257364, 27251.516128,
               27484.969159, 27718.840943, 28167.073648, 28152.669654, 28343.018337, 28557.019692]

vaz_afl = []
for i in range(int(len(vaz_afl_aux))):
    aux = vaz_afl_aux[i] / 10.
    vaz_afl.append(aux)

vt_max = [[489, 493, 496, 498, 502, 507, 513, 517, 521, 525, 528, 531, 534, 537, 540, 545, 550, 556, 561, 565, 571, 577,
           580, 582, 585, 587, 590, 593, 596, 599, 603, 607, 612, 612, 613, 614],
          [489, 493, 496, 498, 502, 507, 513, 517, 521, 525, 528, 531, 534, 537, 540, 545, 550, 556, 561, 565, 571, 577,
           580, 582, 585, 587, 590, 593, 596, 599, 603, 607, 612, 612, 613, 614],
          [489, 493, 496, 498, 502, 507, 513, 517, 521, 525, 528, 531, 534, 537, 540, 545, 550, 556, 561, 565, 571, 577,
           580, 582, 585, 587, 590, 593, 596, 599, 603, 607, 612, 612, 613, 614],
          [489, 493, 496, 498, 502, 507, 513, 517, 521, 525, 528, 531, 534, 537, 540, 545, 550, 556, 561, 565, 571, 577,
           580, 582, 585, 587, 590, 593, 596, 599, 603, 607, 612, 612, 613, 614],
          [489, 493, 496, 498, 502, 507, 513, 517, 521, 525, 528, 531, 534, 537, 540, 545, 550, 556, 561, 565, 571, 577,
           580, 582, 585, 587, 590, 593, 596, 599, 603, 607, 612, 612, 613, 614]]


# Adapt case test data to data class


@dataclass
class ClassUHEData:
    dr_man: np.ndarray
    rfo_dia: np.ndarray
    vaz_afl: list


UHE_Data = ClassUHEData(dr_man=maintenance_duration, rfo_dia=rfo, vaz_afl=vaz_afl)


@dataclass
class ClassVTData:
    vt_max: list


VT_Data = ClassVTData(vt_max=vt_max)

# ACO application

maintenance_duration = UHE_Data.dr_man
n_ug = n_ug                  # number of generating units
n_days = n_days              # number of days
ind_size = n_ug              # individual size
n_ind = 100                  # denotes population size
n_gen = 20                   # denotes number of generations (iterations)

n_lost = 20  # rate of individuals that don't follow the pheromone
rho = 0.2    # evaporation rate

defined_calendar = np.zeros(shape=(n_ug, n_days))

# first optimization
Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                            previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

arr = Agenda.Operacao

original_operation = Agenda.Operacao
original_spilled = Agenda.Vertido
evolutions = []

ACO_base = MetaHeuristics(uhe_data=UHE_Data, n_ug=n_ug, n_days=n_days,
                          maintenance_round=0, maintenance_duration=maintenance_duration,
                          previous_calendar=defined_calendar, n_ind=n_ind,
                          prohibited_start=0, prohibited_end=0,
                          full_year=True, changed_year=False, create_start_individual=True)

number_of_runs = 1000
maintenance_result = np.zeros(shape=(n_ug, number_of_runs))

for run in range(number_of_runs):
    for current_round in range(n_rounds):
        print('Maintenance Round: %i' % (current_round + 1))
        maintenance_round = current_round

        ACO = MetaHeuristics(uhe_data=UHE_Data, n_ug=n_ug, n_days=n_days,
                             maintenance_round=maintenance_round, maintenance_duration=maintenance_duration,
                             previous_calendar=defined_calendar, n_ind=n_ind,
                             prohibited_start=0, prohibited_end=0,
                             full_year=True, changed_year=False, create_start_individual=True)
        ACO.possible_days = ACO_base.possible_days
        ACO.dict_of_days = ACO_base.dict_of_days
        ACO.start_individuals = ACO_base.start_individuals

        start = timeit.default_timer()
        ACO.ant_colony_optimization(uhe_data=UHE_Data, vt_data=VT_Data, n_gen=n_gen, n_ind=n_ind, n_lost=n_lost, rho=rho,
                                    original_operation=original_operation, original_spill=original_spilled)

        stop = timeit.default_timer()
        time = stop - start
        print('Ant Colony Optimization Completed: %4.2f s' % time)

        # update with the run maintenance result
        maintenance_result[:, run] = ACO.best_individual

vertimentos = []

for run in range(number_of_runs):
    maintenance = maintenance_result[:, run]
    current_maintenance = maintenance_duration[:, 0]
    defined_calendar = np.zeros(shape=(n_ug, n_days))

    for ug in range(n_ug):
        m = int(current_maintenance[ug])
        start = int(maintenance[ug])

        defined_calendar[ug, start:start + m] = 1

    Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                                previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)
    vertimentos.append(sum(Agenda.Vertido))
