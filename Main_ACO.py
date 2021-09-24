# Import modules and packages

from meta_heuristics import MetaHeuristics
from Parametros_UHE import Leitura, Volume_Turbinado
import numpy as np
import timeit
import os
from Agenda_OTM import Optimize_Operation
from Display_Resultados import plota_Agenda
from Simula_FID import Calculo_Indicadores
from Results_Excel import Results
import matplotlib.pyplot as plt
from datetime import date

# User Data Input #

initial_date = date(2021, 8, 1)  # start day of the simulation
final_date = date(2022, 7, 31)   # final day of the simulation

# initial_date = date(2021, 1, 1)  # start day of the simulation
# final_date = date(2021, 12, 31)   # final day of the simulation

time_delta = final_date - initial_date
days_range = time_delta.days + 1  # number of simulation days

initial_year = initial_date.year
time_delta_from_first_day = initial_date - date(initial_year, 1, 1)
current_day = time_delta_from_first_day.days  # number of the day in the initial date (year 1)

final_year = final_date.year
time_delta_from_final_day = final_date - date(final_year, 1, 1)
final_day = time_delta_from_final_day.days  # number of the day in the initial date (year 1 or 2)

year_1 = np.arange(current_day, 365)
year_2 = np.arange(0, final_day + 1)

if len(year_1) == len(year_2):
    changed_year = False
    full_year = year_1
else:
    changed_year = True
    full_year = np.concatenate((year_1, year_2))

# Are there any prohibited areas for maintenance?

# prohibited_start_day = date(2021, 1, 10)
# prohibited_end_day = date(2021, 6, 1)

prohibited_start_day = date(2022, 1, 10)
prohibited_end_day = date(2022, 6, 1)

time_delta_from_first_day = prohibited_start_day - initial_date
time_delta_from_final_day = prohibited_end_day - initial_date

prohibited_start = int(time_delta_from_first_day.days)
prohibited_end = int(time_delta_from_final_day.days)

# UHE Data Read

print('Begin Data Reading')
start = timeit.default_timer()

dir_name = 'Excel_Sheets'
main_path = os.path.realpath(dir_name)

path_hydrology = main_path + '/Hydrology.xlsx'
path_maintenance = main_path + '/Maintenance_Duration.xlsx'
path_rfo = main_path + '/Data_Mining_SAMUG.xlsx'
path_pdf = main_path + '/Data_Mining_SAMUG_SMC.xlsx'

UHE_Data = Leitura(path_vazao=path_hydrology, path_manutencao=path_maintenance,
                   path_rfo=path_rfo, path_pdf=path_pdf, calendario_def=None, year_array=full_year)

print('- Files Reading Completed')

# Max Daily Turbined Flow

VT_Data = Volume_Turbinado(UHE_Data.vaz_afl, UHE_Data.lista_turbinas)
print('- Max Daily Turbined Flow Calculated')

stop = timeit.default_timer()
time = stop - start
print('Data Reading Completed: %4.2f s' % time)

# UHE_Data.parameters_plot(VT_Data.vt_max)  # plot inflow and max turbined

# ACO inputs

maintenance_duration = UHE_Data.dr_man
n_ug = 50                    # number of generating units
n_days = len(full_year)      # number of days
ind_size = n_ug              # individual size
n_ind = 100                  # denotes population size
n_gen = 20                   # denotes number of generations (iterations)

n_lost = 20  # rate of individuals that don't follow the pheromone
rho = 0.2    # evaporation rate

n_rounds = maintenance_duration.shape[1]     # number of maintenance rounds

maintenance_result = np.zeros(shape=(n_ug, n_rounds))
defined_calendar = np.zeros(shape=(n_ug, n_days))

# first optimization
Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                            previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

arr = Agenda.Operacao

original_operation = Agenda.Operacao
original_spilled = Agenda.Vertido
evolutions = []

for current_round in range(n_rounds):
    print('Maintenance Round: %i' % (current_round + 1))
    maintenance_round = current_round

    ACO = MetaHeuristics(uhe_data=UHE_Data, n_ug=n_ug, n_days=n_days,
                         maintenance_round=maintenance_round, maintenance_duration=maintenance_duration,
                         previous_calendar=defined_calendar, n_ind=n_ind,
                         prohibited_start=prohibited_start, prohibited_end=prohibited_end,
                         full_year=full_year, changed_year=changed_year)

    start = timeit.default_timer()
    ACO.ant_colony_optimization(uhe_data=UHE_Data, vt_data=VT_Data, n_gen=n_gen, n_ind=n_ind, n_lost=n_lost, rho=rho,
                                original_operation=original_operation, original_spill=original_spilled)

    stop = timeit.default_timer()
    time = stop - start
    print('Ant Colony Optimization Completed: %4.2f s' % time)

    # update calendar with current maintenance result
    maintenance_result[:, current_round] = ACO.best_individual
    current_maintenance = maintenance_duration[:, maintenance_round]

    for ug in range(n_ug):
        m = int(current_maintenance[ug])
        start = int(ACO.best_individual[ug])

        defined_calendar[ug, start:start + m] = 1

    Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                                previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

    original_operation = Agenda.Operacao
    original_spilled = Agenda.Vertido

Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                            previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

plota_Agenda(Agenda.Turbinado, Agenda.Vertido, UHE_Data.vaz_afl, Agenda.Operacao, Agenda.Agenda, UHE_Data.rfo_dia,
             vert_turb=True, ug_op_man=True, vert_n_turb=False, calendario=False)

# evaluate best individual evolution

check_individual_evolution = False
if check_individual_evolution:
    current_maintenance = maintenance_duration[:, 0]
    defined_calendar = np.zeros(shape=(n_ug, n_days))
    fobs = []

    inflow = UHE_Data.vaz_afl

    for best_individual in ACO.best_individual_evolution:
        defined_calendar = np.zeros(shape=(n_ug, n_days))
        for ug in range(n_ug):
            m = int(current_maintenance[ug])
            start = int(best_individual[ug])
            defined_calendar[ug, start:start + m] = 1

        Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                                    previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

        fobs.append(sum(Agenda.Vertido))

    x = np.arange(1, n_gen + 1, 1)
    plt.plot(x, fobs)
    plt.xticks(x)
    plt.xlabel('Generation')
    plt.ylabel('Spill')
    plt.show()

# HDF and HDP indexes

Indexes = Calculo_Indicadores(Agenda, UHE_Data, VT_Data)
print("HDF: ", sum(Indexes.HDF_mes))
print("HDP: ", sum(Indexes.HDP_mes))

plot_indexes = False

if plot_indexes:
    x = np.arange(1, 13, 1)
    plt.figure()
    plt.bar(x, Indexes.HDF_mes, color='blue')
    plt.title('Projeção de HDF')
    plt.xlabel('Mês')
    plt.ylabel('HDF')
    plt.show()

    plt.figure()
    plt.bar(x, Indexes.HDP_mes, color='orange')
    plt.title('Projeção de HDP')
    plt.xlabel('Mês')
    plt.ylabel('HDP')
    plt.show()

# export excel results
export_excel = True

if export_excel:
    Results(Indicadores=Indexes, UHE_Data=UHE_Data, Agenda=Agenda, path_maintenance=path_maintenance,
            n_days=n_days, initial_date=initial_date)
