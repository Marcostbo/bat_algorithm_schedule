# Import modules and packages

from meta_heuristics import BatAlgorithm
from Parametros_UHE import Leitura, Volume_Turbinado
import timeit
import os
import numpy as np
from Agenda_OTM import Optimize_Operation
from Display_Resultados import plota_Agenda

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
                   path_rfo=path_rfo, path_pdf=path_pdf, calendario_def=None)

print('- Files Reading Completed')

# Max Daily Turbined Flow

VT_Data = Volume_Turbinado(UHE_Data.vaz_afl, UHE_Data.lista_turbinas)
print('- Max Daily Turbined Flow Calculated')

stop = timeit.default_timer()
time = stop - start
print('Data Reading Completed: %4.2f s' % time)

# bat algorithm application

maintenance_duration = UHE_Data.dr_man
n_ug = 50         # number of generating units
n_days = 365      # number of days
ind_size = n_ug   # individual size
n_ind = 10        # denotes population size,
n_gen = 5         # denotes number of generations (iterations),

alpha = 0.6   # sound wave amplitude decrease rate
lbd = 0.1     # sound wave pulse emission increase rate

n_rounds = 1
n_bat_rounds = 20
maintenance_result = np.zeros(shape=(n_ug, n_rounds))
defined_calendar = np.zeros(shape=(n_ug, n_days))

for current_round in range(n_rounds):
    print('Maintenance Round: %i' % (current_round + 1))
    maintenance_round = current_round
    Bat = BatAlgorithm(uhe_data=UHE_Data, n_ug=n_ug, n_days=n_days,
                       maintenance_round=maintenance_round, maintenance_duration=maintenance_duration,
                       previous_calendar=defined_calendar, n_ind=n_ind)

    bat_maintenance = []
    bat_fobs = []
    for bat_round in range(n_bat_rounds):
        start = timeit.default_timer()
        Bat.bat_algorithm_process(uhe_data=UHE_Data, previous_calendar=defined_calendar, vt_data=VT_Data,
                                  n_gen=n_gen, alpha=alpha, lbd=lbd, n_ind=n_ind, maintenance_round=current_round)

        stop = timeit.default_timer()
        time = stop - start
        print('Bat Algorithm Completed: %4.2f s' % time)

        bat_maintenance.append(Bat.best_bat_result)
        bat_fobs.append(Bat.best_fob_result)

bat_fobs_array = np.asarray(bat_fobs)
bat_maintenance_array = np.zeros(shape=(n_bat_rounds, n_ug))
for bat_round in range(n_bat_rounds):
    bat_maintenance_array[bat_round, :] = bat_maintenance[bat_round]
