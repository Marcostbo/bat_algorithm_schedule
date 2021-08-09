import numpy as np
import random
from Agenda_OTM import Optimize_Operation


class BatAlgorithm(object):

    def __init__(self, uhe_data, n_ug, n_days, maintenance_round, maintenance_duration, previous_calendar,
                 n_ind):

        self.start_individuals = {}
        self.possible_days = None
        self.dict_of_days = None

        self.best_fob_result = None
        self.best_bat_result = None
        self.evolution = None

        self.n_ug = n_ug
        self.n_days = n_days
        self.current_round = maintenance_round
        self.maintenance_duration = maintenance_duration

        self.initialize_individual(uhe_data=uhe_data, previous_calendar=previous_calendar, n_ind=n_ind)

    def initialize_individual(self, uhe_data, previous_calendar, n_ind):

        dict_of_days = {}
        maintenance_round = self.current_round
        current_maintenance = self.maintenance_duration[:, maintenance_round]
        self.possible_days = np.zeros(shape=(self.n_ug, self.n_days))

        for ug in range(self.n_ug):

            # Select possible days to start maintenance
            maintenance = int(current_maintenance[ug])

            # rfo limitation
            ug_rfo = uhe_data.rfo_dia[ug, :]
            for day in range(self.n_days):
                if ug_rfo[day] == 1:  # Days with rfo are not possible
                    if day - maintenance > 0:
                        self.possible_days[ug, day - maintenance: day] = 1
                    else:
                        self.possible_days[ug, 0:day] = 1
            self.possible_days[ug, self.n_days - maintenance:self.n_days] = 1  # Maintenance must be completed

            # maintenance limitation
            ug_previous_calendar = previous_calendar[ug, :]
            for day in range(self.n_days):
                if ug_previous_calendar[day] == 1:  # Days with maintenance are not possible
                    if day - maintenance > 0:
                        self.possible_days[ug, day - maintenance: day] = 1
                    else:
                        self.possible_days[ug, 0:day] = 1
            self.possible_days[ug, self.n_days - maintenance:self.n_days] = 1

            # Maintenance start for each ug
            list_of_days = []
            for day in range(self.n_days):
                if self.possible_days[ug, day] == 0:
                    list_of_days.append(day)

            dict_of_days[ug] = list_of_days

        # Initialize heuristic individuals
        self.dict_of_days = dict_of_days
        individuals = {}

        for ind in range(n_ind):
            individual = np.zeros(shape=(self.n_ug, self.n_days))
            individuals[ind] = {}
            start_days = []
            for ug in range(self.n_ug):
                maintenance = int(current_maintenance[ug])
                possible_days = dict_of_days[ug]
                start_day = random.choice(possible_days)
                start_days.append(start_day)
                individual[ug, start_day:start_day + maintenance] = 1

            individuals[ind]['start_days'] = start_days
            individuals[ind]['calendar'] = individual

        self.start_individuals = individuals

    @staticmethod
    def check_bat_bounds(n_ug, current_bat, upper_lim, lower_lim, dict_of_days):
        for ug in range(n_ug):
            days = dict_of_days[ug]
            if current_bat[ug] > upper_lim[ug]:
                current_bat[ug] = upper_lim[ug]

            if current_bat[ug] < lower_lim:
                current_bat[ug] = lower_lim

            if int(current_bat[ug]) not in days:
                array = np.asarray(days)
                value = current_bat[ug]
                idx = (np.abs(array - value)).argmin()
                current_bat[ug] = array[idx]

        return current_bat

    def bat_algorithm_process(self, uhe_data, previous_calendar, vt_data, n_gen, alpha, lbd, n_ind):

        ind_size = self.n_ug  # individual size
        pop_size = n_ind      # denotes population size,

        t = 1                                     # iteration count
        a_loud = np.ones(pop_size)                # initial loudness
        r = (1 - np.exp(-lbd * t)) * a_loud       # initial pulse rates
        v = np.zeros(shape=(pop_size, ind_size))  # initial speeds

        lower_lim = 0
        upper_lim = []

        current_maintenance = self.maintenance_duration[:, self.current_round]

        for ug in range(self.n_ug):
            upper_lim.append(self.n_days - current_maintenance[ug])

        fobs = []
        individuals = self.start_individuals
        for individual in individuals.values():
            defined_calendar = individual['calendar']
            agenda = Optimize_Operation(uhe_data, vt_data, calendar=defined_calendar,
                                        previous_calendar=previous_calendar, n_days=self.n_days, n_ug=self.n_ug)
            fobs.append(sum(agenda.Vertido))

        # get best initial bat
        best_fob = min(fobs)
        best_bat_idx = fobs.index(best_fob)
        best_bat = individuals[best_bat_idx]['start_days']
        best_bat = np.asarray(best_bat)

        best_fob_result = []
        best_bat_result = []

        for bat_round in range(1):
            self.evolution = [best_fob]
            t = 1
            while t <= n_gen:
                print('----------- Generation %i -----------' % t)
                for ind in range(pop_size):

                    # update bat

                    beta = np.random.random()
                    bat = np.asarray(individuals[ind]['start_days'])
                    v[ind, :] = v[ind, :] + (best_bat - bat) * beta
                    current_bat = bat + v[ind, :]

                    # local search

                    rand = np.random.random()
                    if rand < r[ind]:
                        e = np.ones(ind_size) * np.random.uniform(-1, 1)
                        current_bat = best_bat + e * a_loud[ind]

                    # verify lower and upper violations

                    current_bat = self.check_bat_bounds(n_ug=self.n_ug, current_bat=current_bat,
                                                        upper_lim=upper_lim, lower_lim=lower_lim,
                                                        dict_of_days=self.dict_of_days)

                    # global search

                    bat = np.round(current_bat)  # round to the next integer - in the future use sigmoid instead
                    bat_calendar = np.zeros(shape=(self.n_ug, self.n_days))

                    for ug in range(self.n_ug):
                        maintenance = int(current_maintenance[ug])
                        start_day = int(random.choice(bat))
                        bat_calendar[ug, start_day:start_day + maintenance] = 1

                    agenda = Optimize_Operation(uhe_data, vt_data, calendar=bat_calendar,
                                                previous_calendar=previous_calendar, n_days=self.n_days, n_ug=self.n_ug)
                    current_fob = sum(agenda.Vertido)

                    # update bat parameters

                    rand = np.random.random()
                    if rand < a_loud[ind] and current_fob <= fobs[ind]:
                        individuals[ind]['start_days'] = current_bat
                        r[ind] = (1 - np.exp(-lbd * t))
                        a_loud[ind] = alpha * a_loud[ind]

                    # verify and update the new best fob

                    if current_fob < best_fob:
                        best_fob = current_fob
                        best_bat = current_bat

                self.evolution.append(best_fob)
                t += 1

            best_fob_result = best_fob
            best_bat_result = np.round(best_bat)
            print('-------------------------------------')

        self.best_fob_result = best_fob_result
        self.best_bat_result = best_bat_result
