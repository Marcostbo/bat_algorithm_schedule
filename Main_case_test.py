# Import modules and packages

from Agenda_OTM import Optimize_Operation
import numpy as np
import random
from dataclasses import dataclass

# Case test data

n_days = 36
n_ug = 5
n_rounds = 9

maintenance_duration = [[5, 0, 0, 0, 0, 0, 0, 0, 0],
                        [8, 0, 0, 0, 0, 0, 0, 0, 0],
                        [6, 0, 0, 0, 0, 0, 0, 0, 0],
                        [6, 0, 0, 0, 0, 0, 0, 0, 0],
                        [3, 0, 0, 0, 0, 0, 0, 0, 0]]

a = np.sort(maintenance_duration)
dm_sort = np.zeros(shape=(n_ug, n_rounds))
for im in range(n_rounds):
    for it in range(n_ug):
        dm_sort[it, im] = int(a[it, n_rounds - im - 1])
maintenance_duration = dm_sort

rfo = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

rfo = np.array(rfo)

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

# Select possible days of maintenance for each ug

dict_of_days = {}
maintenance_round = 0
current_maintenances = maintenance_duration[:, maintenance_round]
possible_days = np.zeros(shape=(n_ug, n_days))

for ug in range(n_ug):
    # Select possible days to start maintenance
    maintenance = int(current_maintenances[ug])
    ug_rfo = rfo[ug, :]
    for day in range(n_days):
        if ug_rfo[day] == 1:  # Days with rfo are not possible
            possible_days[ug, day - maintenance: day + 1] = 1
    possible_days[ug, n_days - maintenance:n_days] = 1  # Maintenance must be completed

    # Maintenance start for each ug
    list_of_days = []
    for day in range(n_days):
        if possible_days[ug, day] == 0:
            list_of_days.append(day)

    dict_of_days[ug] = list_of_days

# Initialize heuristic individuals

individuals = {}
n_ind = 50

for ind in range(n_ind):
    individual = np.zeros(shape=(n_ug, n_days))
    individuals[ind] = {}
    start_days = []
    for ug in range(n_ug):
        maintenance = int(current_maintenances[ug])
        possible_days = dict_of_days[ug]
        start_day = random.choice(possible_days)
        start_days.append(start_day)
        individual[ug, start_day:start_day + maintenance] = 1

    individuals[ind]['start_days'] = start_days
    individuals[ind]['calendar'] = individual


# Define important functions


def get_best_bat(current_fobs, current_individuals):
    current_best_fob = min(current_fobs)
    current_best_bat_idx = current_fobs.index(current_best_fob)
    current_best_bat = current_individuals[current_best_bat_idx]['start_days']

    return current_best_bat, current_best_fob


def verify_bounds(val, lower, upper):
    if val < lower:
        val = lower
    if val > upper:
        val = upper
    return val


# Initialize BAT algorithm

ind_size = n_ug   # individual size
pop_size = n_ind  # denotes population size,
n_gen = 10        # denotes number of generations (iterations),

alpha = 0.6   # sound wave amplitude decrease rate
lbd = 0.1     # sound wave pulse emission increase rate
beta_min = 0  # minimum frequency
beta_max = 1  # maximum frequency

t = 1                           # iteration count
A = np.ones(pop_size)           # initial loudness
r = (1 - np.exp(-lbd * t)) * A  # initial pulse rates
v = np.zeros(shape=(pop_size, ind_size))  # initial speeds

lower_lim = 0
upper_lim = n_days - 1

fobs = []
for individual in individuals.values():
    defined_calendar = individual['calendar']
    Agenda = Optimize_Operation(UHE_Data, VT_Data, calendar=defined_calendar, n_days=n_days, n_ug=n_ug)
    fobs.append(sum(Agenda.Vertido))

best_bat, best_fob = get_best_bat(current_fobs=fobs, current_individuals=individuals)  # best initial bat
best_bat = np.asarray(best_bat)

best_fob_result = []
best_bat_result = []

for bat_round in range(1):
    print('-------------- Round %i --------------' % (bat_round + 1))
    evolution = [best_fob]
    t = 1
    while t <= n_gen:
        for ind in range(pop_size):

            print('Evaluation of Bat %i in %i Generation' % ((ind + 1), t))

            # update bat

            beta = np.random.random()
            bat = np.asarray(individuals[ind]['start_days'])
            v[ind, :] = v[ind, :] + (best_bat - bat) * beta
            current_bat = bat + v[ind, :]

            # local search

            rand = np.random.random()
            if rand < r[ind]:
                e = np.ones(ind_size) * np.random.uniform(-1, 1)
                current_bat = best_bat + e * A[ind]

            # verify lower and upper violations

            current_bat = np.where(current_bat > upper_lim, upper_lim, current_bat)
            current_bat = np.where(current_bat < lower_lim, 0, current_bat)

            # global search

            bat = np.round(current_bat)  # round to the next integer - in the future use sigmoid instead
            bat_calendar = np.zeros(shape=(n_ug, n_days))
            for ug in range(n_ug):
                maintenance = int(current_maintenances[ug])
                start_day = int(random.choice(bat))
                bat_calendar[ug, start_day:start_day + maintenance] = 1

            Agenda = Optimize_Operation(UHE_Data, VT_Data, calendar=bat_calendar, n_days=n_days, n_ug=n_ug)
            current_fob = sum(Agenda.Vertido)

            # update bat parameters

            rand = np.random.random()
            if rand < A[ind] and current_fob <= fobs[ind]:
                individuals[ind]['start_days'] = current_bat
                r[ind] = (1 - np.exp(-lbd * t))
                A[ind] = alpha * A[ind]

            # verify and update the new best fob

            if current_fob < best_fob:
                best_fob = current_fob
                best_bat = current_bat

        t += 1

        evolution.append(best_fob)

    best_fob_result.append(best_fob)
    best_bat_result.append(best_bat)

    print('-------------------------------------')
